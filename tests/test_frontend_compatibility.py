import pytest
from fastapi.testclient import TestClient
from app import app
from src.schemas.chat_schema import ChatResponseData
from src.schemas.mbti_schema import MBTIQuestion, MBTISubmitRequest
from src.schemas.prediction_schema import AdmissionChanceRequest


@pytest.fixture
def client():
    return TestClient(app)


def test_chat_response_frontend_compatibility():
    data = ChatResponseData(
        answer="Chào bạn, mình là AI Tuyển sinh UTC.",
        session_id="test-session-123",
        sources=[],
        suggested_questions=["Điểm chuẩn ngành CNTT?"]
    )
    dumped = data.model_dump()
    assert "reply" in dumped
    assert dumped["reply"] == "Chào bạn, mình là AI Tuyển sinh UTC."
    assert dumped["answer"] == dumped["reply"]


def test_mbti_question_frontend_compatibility():
    q = MBTIQuestion(
        id=1,
        text="Bạn thích làm việc độc lập hay theo nhóm?",
        dimension="EI",
        positive_trait="E",
    )
    dumped = q.model_dump()
    assert dumped["question"] == "Bạn thích làm việc độc lập hay theo nhóm?"
    assert dumped["option_a"]["text"] == "Đồng ý"
    assert dumped["option_a"]["trait"] == "E"
    assert dumped["option_b"]["text"] == "Không đồng ý"
    assert dumped["option_b"]["trait"] == "I"


def test_mbti_submit_string_answers_a_b(client):
    payload = {
        "studentName": "Nguyễn Văn A",
        "answers": {
            "1": "A",
            "2": "B",
            "3": "A",
            "4": "B"
        }
    }
    req = MBTISubmitRequest(**payload)
    assert len(req.answers) == 4
    scores = {item.question_id: item.score for item in req.answers}
    assert scores[1] == 5
    assert scores[2] == 1
    assert scores[3] == 5
    assert scores[4] == 1

    resp = client.post("/api/mbti/submit", json=payload)
    assert resp.status_code == 200
    res_data = resp.json()["data"]
    assert "title" in res_data
    assert "description" in res_data
    assert "work_environment" in res_data
    assert "scores" in res_data
    assert "E" in res_data["scores"]
    assert "I" in res_data["scores"]
    assert len(res_data["recommended_majors"]) > 0
    rec0 = res_data["recommended_majors"][0]
    assert "ma_chuong_trinh" in rec0
    assert "ten_chuong_trinh" in rec0


def test_evaluate_chance_frontend_payload(client):
    frontend_payload = {
        "ma_chuong_trinh": "GHA14",
        "ma_to_hop": "A00",
        "diem_xet_tuyen": 26.5,
        "khu_vuc": "KV1"
    }
    req = AdmissionChanceRequest(**frontend_payload)
    assert req.target_major_code == "GHA14"
    assert req.priority_region == "KV1"
    assert "toan" in req.academic_scores
    assert "vat_ly" in req.academic_scores
    assert "hoa_hoc" in req.academic_scores

    resp = client.post("/api/predict/admission-chance", json=frontend_payload)
    assert resp.status_code == 200
    res_json = resp.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert "chance_percentage" in data
    assert "evaluation" in data
    assert data["chance_percentage"] == data["xac_suat_trung_tuyen"]
    assert data["evaluation"] == data["nhan_xet_chuyen_gia"]
    assert data["chance_percentage"] > 0


def test_evaluate_chance_legacy_moet_code(client):
    frontend_payload = {
        "ma_chuong_trinh": "7480201",
        "ma_to_hop": "A00",
        "diem_xet_tuyen": 25.0
    }
    resp = client.post("/api/predict/admission-chance", json=frontend_payload)
    assert resp.status_code == 200
    res_json = resp.json()
    assert res_json["success"] is True
    data = res_json["data"]
    assert data["chance_percentage"] > 0
    assert "evaluation" in data
