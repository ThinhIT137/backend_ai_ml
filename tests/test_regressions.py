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
