import itertools
from unittest.mock import patch
import pytest

from src.schemas.mbti_schema import MBTISubmitRequest
from src.schemas.chat_schema import ChatRequest, KnowledgeCreateRequest
from src.ml.mbti.scorer import MBTI_QUESTIONS, calculate_mbti_result
from src.services.chat_service import chat_service
from src.ml.llm.rag import rag_pipeline, BM25SearchEngine


@pytest.mark.parametrize("letters", list(itertools.product("EI", "SN", "TF", "JP")))
def test_all_mbti_types(letters):
    target = "".join(letters)
    request = MBTISubmitRequest(
        answers=[
            {"question_id": q["id"], "score": 5 if q["positive_trait"] in target else 1}
            for q in MBTI_QUESTIONS
        ]
    )
    assert calculate_mbti_result(request.answers).mbti_type == target


@pytest.mark.parametrize(
    "response",
    [{"choices": []}, {"choices": [{"message": {"content": " "}}]}],
)
def test_llm_empty_response_fallback(response):
    with patch("src.services.chat_service.llm_client.generate", return_value=response), patch.object(
        rag_pipeline, "retrieve", return_value=[]
    ):
        result = chat_service.ask(ChatRequest(question="hoc phi", session_id="session"))
        assert result.answer.strip()
        assert result.session_id == "session"


def test_llm_timeout_fallback():
    with patch("src.services.chat_service.llm_client.generate", side_effect=TimeoutError("timeout")), patch.object(
        rag_pipeline, "retrieve", return_value=[]
    ):
        assert chat_service.ask(ChatRequest(question="hoc phi")).answer.strip()


def test_create_syncs_real_rag():
    item = {
        "ma_tri_thuc": "test",
        "chu_de": "Hoc phi",
        "noi_dung": "hoc phi 100",
        "trang_thai": "active",
    }
    previous = list(rag_pipeline.all_chunks)
    try:
        with patch(
            "src.services.chat_service.chat_repository.create_tri_thuc", return_value=item
        ), patch(
            "src.services.chat_service.chat_repository.get_active_tri_thuc", return_value=[item]
        ):
            chat_service.create_knowledge(KnowledgeCreateRequest(topic="Hoc phi", answer="hoc phi 100"))
            assert rag_pipeline.retrieve("hoc phi")[0]["chunk_id"] == "test"
    finally:
        rag_pipeline.all_chunks = previous
        rag_pipeline.engine = BM25SearchEngine(previous)


def test_knowledge_requires_authorization(client):
    item = {
        "ma_tri_thuc": "test",
        "chu_de": "Hoc phi",
        "noi_dung": "100",
        "trang_thai": "active",
    }
    with patch(
        "src.services.chat_service.chat_repository.create_tri_thuc", return_value=item
    ) as create, patch.object(chat_service, "sync_knowledge"):
        response = client.post("/api/chat/knowledge", json={"topic": "Hoc phi", "answer": "100"})
        assert response.status_code in (401, 403)
        create.assert_not_called()

def test_knowledge_create_with_rag_sync_failure():
    item = {
        "ma_tri_thuc": "test_warn",
        "chu_de": "Hoc bong",
        "cau_hoi_mau": "Co hoc bong khong?",
        "noi_dung": "Co nhieu hoc bong",
        "trang_thai": "active",
    }
    with patch(
        "src.services.chat_service.chat_repository.create_tri_thuc", return_value=item
    ), patch.object(
        chat_service, "sync_knowledge", side_effect=RuntimeError("Gemini sync error")
    ):
        res = chat_service.create_knowledge(KnowledgeCreateRequest(topic="Hoc bong", answer="Co nhieu hoc bong"))
        assert res.sync_warning is not None
        assert "đồng bộ RAG thất bại" in res.sync_warning
        assert res.syncWarning == res.sync_warning
        dumped = res.model_dump(mode="json")
        assert dumped["syncWarning"] is not None


def test_knowledge_api_sync_warning_contract(client):
    item = {
        "ma_tri_thuc": "test_api_warn",
        "chu_de": "Hoc bong",
        "cau_hoi_mau": "Co hoc bong khong?",
        "noi_dung": "Co nhieu hoc bong",
        "trang_thai": "active",
    }
    with patch(
        "src.services.chat_service.chat_repository.create_tri_thuc", return_value=item
    ), patch.object(
        chat_service, "sync_knowledge", side_effect=RuntimeError("Chroma/Gemini error")
    ):
        auth_token_type = "Bearer"
        headers = {"Authorization": f"{auth_token_type} internal_secret_test_key"}
        response = client.post(
            "/api/chat/knowledge",
            json={"topic": "Hoc bong", "answer": "Co nhieu hoc bong"},
            headers=headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["syncWarning"] is not None
        assert "đồng bộ RAG thất bại" in data["syncWarning"]


def test_mbti_identity_data_masking_public_vs_internal(client, sample_mbti_answers_list):
    body = {
        "studentName": "Nguyen Van A",
        "sessionId": "sess_mask_test",
        "cccd": "001204008899",
        "answers": sample_mbti_answers_list,
        "include_ai_advice": False,
    }
    submit_res = client.post("/api/mbti/submit", json=body)
    assert submit_res.status_code == 200
    sub_data = submit_res.json()["data"]
    assert sub_data["cccd"] == "0012******99"
    res_id = sub_data["result_id"]

    if res_id:
        public_res = client.get(f"/api/mbti/result/{res_id}")
        assert public_res.status_code == 200
        assert public_res.json()["data"]["cccd"] == "0012******99"

        internal_res = client.get(
            f"/api/mbti/result/{res_id}",
            headers={"Authorization": f"{'Bearer'} internal_secret_test_key"},
        )
        assert internal_res.status_code == 200
        assert internal_res.json()["data"]["cccd"] == "001204008899"


def test_mbti_history_query_validation(client):
    res_invalid = client.get("/api/mbti/history?cccd=invalid'--")
    assert res_invalid.status_code == 422
