import pytest
from unittest.mock import patch, MagicMock


def test_root_endpoint(client):
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "UTC" in data["message"] or "Microservice" in data["message"]
    assert data["docs"] == "/docs"


def test_health_endpoint(client):
    response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["status"] == "healthy"
    assert "version" in payload["data"]


def test_mbti_questions_endpoint(client):
    response = client.get("/api/mbti/questions")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["total"] in [20, 28]
    assert len(payload["data"]) == payload["total"]
    first = payload["data"][0]
    assert "id" in first
    assert "text" in first
    assert "dimension" in first


def test_mbti_submit_endpoint_list(client, sample_mbti_answers_list):
    body = {
        "studentName": "Trần Văn B",
        "sessionId": "sess_unit_test",
        "cccd": "001203004567",
        "answers": sample_mbti_answers_list,
        "include_ai_advice": False,
    }
    response = client.post("/api/mbti/submit", json=body)
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["mbti_type"] in [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP",
    ]
    assert len(data["recommended_majors"]) > 0
    assert "dimension_scores" in data


def test_mbti_submit_endpoint_dict(client, sample_mbti_answers_dict):
    body = {
        "answers": sample_mbti_answers_dict,
        "include_ai_advice": False,
    }
    response = client.post("/api/mbti/submit", json=body)
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["mbti_type"] is not None


def test_mbti_submit_invalid_question_id(client):
    body = {
        "answers": [
            {"question_id": 999, "score": 5},
            {"question_id": 1, "score": 4},
            {"question_id": 2, "score": 3},
            {"question_id": 3, "score": 2},
        ]
    }
    response = client.post("/api/mbti/submit", json=body)
    assert response.status_code == 422


def test_mbti_submit_duplicate_question_id(client):
    body = {
        "answers": [
            {"question_id": 1, "score": 5},
            {"question_id": 1, "score": 4},
            {"question_id": 2, "score": 3},
            {"question_id": 3, "score": 2},
        ]
    }
    response = client.post("/api/mbti/submit", json=body)
    assert response.status_code == 422


def test_mbti_submit_empty_answers(client):
    body = {"answers": []}
    response = client.post("/api/mbti/submit", json=body)
    assert response.status_code == 422


def test_mbti_get_result_found(client, sample_mbti_answers_list):
    submit_res = client.post("/api/mbti/submit", json={"answers": sample_mbti_answers_list})
    assert submit_res.status_code == 200
    res_id = submit_res.json()["data"]["result_id"]

    if res_id:
        get_res = client.get(f"/api/mbti/result/{res_id}")
        assert get_res.status_code == 200
        assert get_res.json()["success"] is True


def test_mbti_get_result_not_found(client):
    response = client.get("/api/mbti/result/00000000-0000-0000-0000-000000000000")
    assert response.status_code == 404


def test_mbti_history_with_session_id(client):
    response = client.get("/api/mbti/history?session_id=sess_unit_test")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)


def test_mbti_history_with_cccd(client):
    response = client.get("/api/mbti/history?cccd=001203004567")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)


def test_mbti_history_without_params(client):
    response = client.get("/api/mbti/history")
    assert response.status_code == 422


def test_predict_all_benchmarks(client):
    response = client.get("/api/predict/all-benchmarks")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["total"] == 54
    assert len(payload["data"]) == 54

    item = payload["data"][0]
    assert "ma_chuong_trinh" in item
    assert "diem_du_doan_2026" in item
    assert "phuong_thuc_quy_doi" in item


def test_predict_benchmark_by_major_found(client):
    response = client.get("/api/predict/benchmark/GHA14")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["ma_chuong_trinh"] == "GHA14"
    assert data["ten_chuong_trinh"] == "Công nghệ thông tin"
    assert "pt1_thpt" in data["phuong_thuc_quy_doi"]
    assert "pt2_hoc_ba" in data["phuong_thuc_quy_doi"]


def test_predict_benchmark_by_major_not_found(client):
    response = client.get("/api/predict/benchmark/INVALID_MAJOR_CODE")
    assert response.status_code == 404


def test_predict_simulate_scenario_valid(client):
    body = {
        "ma_chuong_trinh": "GHA14",
        "custom_quota_growth": 0.1,
        "custom_macro_delta": -0.2,
    }
    response = client.post("/api/predict/simulate-scenario", json=body)
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["ma_chuong_trinh"] == "GHA14"
    assert 15.0 <= payload["data"]["diem_du_doan_2026"] <= 29.5


def test_predict_simulate_scenario_not_found(client):
    body = {
        "ma_chuong_trinh": "NONEXISTENT",
        "custom_quota_growth": 0.0,
    }
    response = client.post("/api/predict/simulate-scenario", json=body)
    assert response.status_code == 404


def test_predict_admission_chance_valid(client, sample_academic_scores):
    body = {
        "academic_scores": sample_academic_scores,
        "target_major_code": "GHA14",
        "admission_method": "PT1",
        "priority_region": "KV2",
    }
    response = client.post("/api/predict/admission-chance", json=body)
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["ma_chuong_trinh"] == "GHA14"
    assert data["to_hop_toi_uu"] in ["A00", "A01", "D01", "D07"]
    assert 0.0 <= data["xac_suat_trung_tuyen"] <= 100.0
    assert data["muc_do_an_toan"] in ["RẤT_CAO", "CAO", "TRUNG_BÌNH", "THẤP", "RẤT_THẤP"]
    assert len(data["nhan_xet_chuyen_gia"]) > 0


def test_predict_admission_chance_with_ielts(client, sample_academic_scores):
    body = {
        "academic_scores": sample_academic_scores,
        "target_major_code": "GHA14",
        "priority_region": "KV3",
        "foreign_language_cert": {
            "cert_type": "IELTS",
            "score": 7.5,
        },
    }
    response = client.post("/api/predict/admission-chance", json=body)
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert payload["data"]["tong_diem_xet_tuyen"] > 0


def test_predict_admission_chance_invalid_major(client, sample_academic_scores):
    body = {
        "academic_scores": sample_academic_scores,
        "target_major_code": "XYZ999",
    }
    response = client.post("/api/predict/admission-chance", json=body)
    assert response.status_code == 404


def test_predict_recommend_majors_valid(client, sample_academic_scores):
    body = {
        "academic_scores": sample_academic_scores,
        "priority_region": "KV2-NT",
        "priority_group": "UT1",
    }
    response = client.post("/api/predict/recommend-majors", json=body)
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    data = payload["data"]
    assert data["total_majors_evaluated"] == 54
    assert "safety_tier" in data
    assert "target_tier" in data
    assert "dream_tier" in data
    assert len(data["strategic_advice"]) > 0


def test_chat_endpoint_valid_question(client):
    body = {
        "message": "Trường ĐH Giao thông Vận tải có bao nhiêu phương thức xét tuyển?",
        "session_id": "test_session_chat",
    }
    mock_resp = {
        "choices": [
            {"message": {"content": "Trường ĐH Giao thông Vận tải có 4 phương thức xét tuyển chính."}}
        ]
    }
    with patch("src.services.chat_service.llm_client.generate", return_value=mock_resp):
        response = client.post("/api/chat", json=body)
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        data = payload["data"]
        assert len(data["answer"]) > 0
        assert data["session_id"] == "test_session_chat"
        assert isinstance(data["suggested_questions"], list)


def test_chat_endpoint_question_alias(client):
    body = {
        "question": "Điểm chuẩn ngành Kỹ thuật ô tô năm 2025?",
    }
    mock_resp = {
        "choices": [
            {"message": {"content": "Điểm chuẩn ngành Kỹ thuật ô tô năm 2025 là 24.50 điểm."}}
        ]
    }
    with patch("src.services.chat_service.llm_client.generate", return_value=mock_resp):
        response = client.post("/api/chat", json=body)
        assert response.status_code == 200
        payload = response.json()
        assert payload["success"] is True
        assert len(payload["data"]["answer"]) > 0


def test_chat_endpoint_empty_message(client):
    body = {"message": "   "}
    response = client.post("/api/chat", json=body)
    assert response.status_code == 422


def test_chat_sync_knowledge(client):
    response = client.post("/api/chat/sync-knowledge")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert "total_documents" in payload


def test_chat_knowledge_list(client):
    response = client.get("/api/chat/knowledge")
    assert response.status_code == 200
    payload = response.json()
    assert payload["success"] is True
    assert isinstance(payload["data"], list)


def test_chat_knowledge_unauthorized(client):
    res_create = client.post(
        "/api/chat/knowledge",
        json={"topic": "Chủ đề test", "answer": "Nội dung"},
    )
    assert res_create.status_code in [401, 403]

    res_update = client.put(
        "/api/chat/knowledge/fake_id",
        json={"topic": "Chủ đề sửa"},
    )
    assert res_update.status_code in [401, 403]

    res_delete = client.delete("/api/chat/knowledge/fake_id")
    assert res_delete.status_code in [401, 403]


def test_chat_knowledge_crud_with_mock(client):
    fake_item = {
        "ma_tri_thuc": "fake_id_123",
        "chu_de": "Chủ đề test",
        "cau_hoi_mau": "Câu hỏi test",
        "noi_dung": "Nội dung test",
        "trang_thai": "active",
        "create_at": "2026-10-09T00:00:00",
    }
    auth_headers = {"Authorization": "Bearer admin_test_token"}

    with patch("src.repositories.chat_repository.chat_repository.create_tri_thuc", return_value=fake_item):
        with patch("src.services.chat_service.chat_service.sync_knowledge"):
            res_create = client.post(
                "/api/chat/knowledge",
                headers=auth_headers,
                json={
                    "topic": "Chủ đề test",
                    "question": "Câu hỏi test",
                    "answer": "Nội dung test",
                },
            )
            assert res_create.status_code == 201
            assert res_create.json()["chu_de"] == "Chủ đề test"

    with patch("src.repositories.chat_repository.chat_repository.update_tri_thuc", return_value=fake_item):
        with patch("src.services.chat_service.chat_service.sync_knowledge"):
            res_update = client.put(
                "/api/chat/knowledge/fake_id_123",
                headers=auth_headers,
                json={"topic": "Chủ đề test sửa"},
            )
            assert res_update.status_code == 200

    with patch("src.repositories.chat_repository.chat_repository.delete_tri_thuc", return_value=True):
        with patch("src.services.chat_service.chat_service.sync_knowledge"):
            res_delete = client.delete("/api/chat/knowledge/fake_id_123", headers=auth_headers)
            assert res_delete.status_code == 200
            assert res_delete.json()["success"] is True


def test_chat_knowledge_update_not_found(client):
    auth_headers = {"Authorization": "Bearer admin_test_token"}
    with patch("src.repositories.chat_repository.chat_repository.update_tri_thuc", return_value=None):
        res = client.put(
            "/api/chat/knowledge/nonexistent_id",
            headers=auth_headers,
            json={"topic": "Test"},
        )
        assert res.status_code == 404


def test_chat_knowledge_delete_not_found(client):
    auth_headers = {"Authorization": "Bearer admin_test_token"}
    with patch("src.repositories.chat_repository.chat_repository.delete_tri_thuc", return_value=False):
        res = client.delete("/api/chat/knowledge/nonexistent_id", headers=auth_headers)
        assert res.status_code == 404
