import uuid
from datetime import datetime
import pytest
from pydantic import ValidationError
from unittest.mock import patch, MagicMock

from src.models.mbti_result import MBTIResultRecord
from src.models.prediction_log import PredictionLogRecord
from src.models.chat_history import ChatHistoryRecord
from src.schemas.mbti_schema import (
    MBTIQuestion,
    MBTIAnswerItem,
    MBTISubmitRequest,
    DimensionScore,
    MajorRecommendation,
    CareerTrajectoryItem,
    MBTIResultData,
)
from src.schemas.prediction_schema import (
    EquivalentMethodScores,
    BenchmarkPredictionItem,
    BenchmarkScenarioRequest,
    ForeignLanguageCert,
    AdmissionChanceRequest,
    MajorChanceResult,
    StrategyTier,
    MajorRecommendationData,
)
from src.schemas.chat_schema import (
    ChatRequest,
    ChatSourceItem,
    KnowledgeItemSchema,
    KnowledgeCreateRequest,
    KnowledgeUpdateRequest,
)
from src.repositories.prediction_repository import (
    PredictionRepository,
    prediction_repository,
)
from src.repositories.major_repository import (
    MajorRepository,
    major_repository,
)
from src.repositories.mbti_repository import (
    MBTIRepository,
    mbti_repository,
)
from src.repositories.chat_repository import (
    ChatRepository,
    chat_repository,
)
from src.services.prediction_service import (
    PredictionService,
    prediction_service,
)
from src.services.mbti_service import (
    MBTIService,
    mbti_service,
)
from src.services.chat_service import (
    ChatService,
    chat_service,
)
from src.core.exceptions import NotFoundException, ValidationException


def test_mbti_result_record_valid():
    rec = MBTIResultRecord(
        ma_ket_qua="res_123",
        session_id="sess_123",
        nhom_tinh_cach="INTJ",
        cccd="012345678901",
        goi_y_nganh={"majors": ["7480201"]},
        create_at=datetime.utcnow(),
    )
    assert rec.ma_ket_qua == "res_123"
    assert rec.nhom_tinh_cach == "INTJ"
    assert rec.cccd == "012345678901"


def test_mbti_result_record_missing_required():
    with pytest.raises(ValidationError):
        MBTIResultRecord(cccd="012345678901")


def test_prediction_log_record_defaults():
    rec = PredictionLogRecord()
    assert rec.evaluation_type == "admission_chance"
    assert rec.admission_method == "PT1"
    assert rec.academic_scores == {}


def test_prediction_log_record_full():
    rec = PredictionLogRecord(
        session_id="sess_pred",
        cccd="012345678901",
        target_major_code="GHA14",
        target_major_name="Công nghệ thông tin",
        academic_scores={"toan": 9.0, "ly": 8.5, "hoa": 8.0},
        calculated_score=25.5,
        predicted_benchmark=25.85,
        admission_probability=82.5,
        risk_level="CAO",
    )
    assert rec.target_major_code == "GHA14"
    assert rec.calculated_score == 25.5
    assert rec.risk_level == "CAO"


def test_chat_history_record_valid():
    rec = ChatHistoryRecord(
        session_id="chat_001",
        sender="user",
        message="Điểm chuẩn ngành CNTT năm 2025 là bao nhiêu?",
    )
    assert rec.session_id == "chat_001"
    assert rec.sender == "user"


def test_mbti_question_schema_validation():
    q = MBTIQuestion(
        id=1,
        text="Bạn thích nghiên cứu lý thuyết hơn thực hành?",
        dimension="SN",
        positive_trait="N",
    )
    assert q.id == 1
    assert q.dimension == "SN"
    assert q.positive_trait == "N"

    with pytest.raises(ValidationError):
        MBTIQuestion(
            id=1,
            text="Invalid trait",
            dimension="SN",
            positive_trait="Z",
        )


def test_mbti_answer_item_score_range():
    ans = MBTIAnswerItem(question_id=1, score=4)
    assert ans.score == 4

    with pytest.raises(ValidationError):
        MBTIAnswerItem(question_id=1, score=6)

    with pytest.raises(ValidationError):
        MBTIAnswerItem(question_id=1, score=0)


def test_mbti_submit_request_normalization():
    req_dict = MBTISubmitRequest(
        student_name="Nguyễn Văn A",
        answers={"1": 5, "2": 4, "3": 3, "4": 2},
    )
    assert len(req_dict.answers) == 4
    assert req_dict.answers[0].question_id == 1
    assert req_dict.answers[0].score == 5

    req_list = MBTISubmitRequest(
        answers=[
            MBTIAnswerItem(question_id=1, score=5),
            MBTIAnswerItem(question_id=2, score=4),
            MBTIAnswerItem(question_id=3, score=3),
            MBTIAnswerItem(question_id=4, score=2),
        ]
    )
    assert len(req_list.answers) == 4


def test_dimension_score_schema():
    ds = DimensionScore(
        extraversion=30.0,
        introversion=70.0,
        sensing=45.0,
        intuition=55.0,
        thinking=80.0,
        feeling=20.0,
        judging=75.0,
        perceiving=25.0,
    )
    assert ds.introversion == 70.0
    assert ds.thinking == 80.0


def test_major_recommendation_schema():
    rec = MajorRecommendation(
        major_code="7480201",
        major_name="Công nghệ thông tin",
        faculty="Khoa Công nghệ thông tin",
        match_score=95,
        reason="Tư duy logic cao, phù hợp lập trình",
    )
    assert rec.major_code == "7480201"
    assert rec.match_score == 95


def test_career_trajectory_schema():
    item = CareerTrajectoryItem(
        phase="0 - 2 năm",
        roles=["Junior Software Engineer"],
        milestone="Nắm vững kỹ thuật lập trình và quy trình Scrum",
    )
    assert item.phase == "0 - 2 năm"
    assert len(item.roles) == 1


def test_mbti_result_data_schema():
    ds = DimensionScore(
        extraversion=30.0,
        introversion=70.0,
        sensing=45.0,
        intuition=55.0,
        thinking=80.0,
        feeling=20.0,
        judging=75.0,
        perceiving=25.0,
    )
    res = MBTIResultData(
        mbti_type="INTJ",
        type_name="Nhà Kiến thiết Hệ thống",
        archetype_group="Nhà Phân tích",
        personality_summary="Chiến lược, độc lập, có tầm nhìn dài hạn",
        strengths=["Tư duy phân tích sắc bén"],
        weaknesses=["Khắt khe"],
        work_style="Độc lập, tập trung cao độ",
        suitable_environment="Môi trường nghiên cứu và phát triển công nghệ cao",
        dimension_scores=ds,
        recommended_majors=[],
    )
    assert res.mbti_type == "INTJ"
    assert res.type_name == "Nhà Kiến thiết Hệ thống"


def test_equivalent_method_scores():
    ems = EquivalentMethodScores(
        pt1_thpt=25.5,
        pt2_hoc_ba=26.8,
        pt3_hsa=105.0,
        pt4_tsa=68.5,
    )
    assert ems.pt1_thpt == 25.5
    assert ems.pt3_hsa == 105.0


def test_benchmark_prediction_item_schema():
    ems = EquivalentMethodScores(
        pt1_thpt=25.5,
        pt2_hoc_ba=26.8,
        pt3_hsa=105.0,
        pt4_tsa=68.5,
    )
    item = BenchmarkPredictionItem(
        ma_chuong_trinh="GHA14",
        ten_chuong_trinh="Công nghệ thông tin",
        diem_chuan_2025=25.85,
        diem_du_doan_2026=26.1,
        score_range_min=25.75,
        score_range_max=26.45,
        trend="TĂNG",
        delta_score=0.25,
        phuong_thuc_quy_doi=ems,
    )
    assert item.ma_chuong_trinh == "GHA14"
    assert item.trend == "TĂNG"


def test_benchmark_scenario_request_validation():
    req = BenchmarkScenarioRequest(
        ma_chuong_trinh="GHA14",
        custom_quota_growth=0.1,
        custom_macro_delta=-0.2,
    )
    assert req.ma_chuong_trinh == "GHA14"
    assert req.custom_quota_growth == 0.1


def test_foreign_language_cert():
    flc = ForeignLanguageCert(cert_type="IELTS", score=7.0)
    assert flc.cert_type == "IELTS"
    assert flc.score == 7.0


def test_admission_chance_request():
    req = AdmissionChanceRequest(
        academic_scores={"toan": 8.5, "ly": 8.0, "hoa": 7.5},
        target_major_code="GHA14",
        priority_region="KV2",
    )
    assert req.priority_region == "KV2"
    assert req.academic_scores["toan"] == 8.5


def test_major_chance_result():
    mcr = MajorChanceResult(
        ma_chuong_trinh="GHA14",
        ten_chuong_trinh="Công nghệ thông tin",
        diem_chuan_du_doan=25.85,
        to_hop_toi_uu="A00",
        diem_to_hop_goc=24.0,
        diem_uu_tien=0.25,
        tong_diem_xet_tuyen=24.25,
        do_lech_diem=-1.6,
        xac_suat_trung_tuyen=42.0,
        muc_do_an_toan="THẤP",
        nhan_xet_chuyen_gia="Cần bổ sung nguyện vọng dự phòng",
    )
    assert mcr.ma_chuong_trinh == "GHA14"
    assert mcr.muc_do_an_toan == "THẤP"


def test_strategy_tier_schema():
    st = StrategyTier(
        tier_name="Giỏ An toàn",
        tier_description="Xác suất đỗ > 85%",
        recommended_nv_slots="NV5 trở đi",
        total_majors=0,
        majors=[],
    )
    assert st.total_majors == 0
    assert st.tier_name == "Giỏ An toàn"


def test_major_recommendation_data_schema():
    st = StrategyTier(
        tier_name="Giỏ An toàn",
        tier_description="Xác suất đỗ > 85%",
        recommended_nv_slots="NV5 trở đi",
        total_majors=0,
        majors=[],
    )
    mrd = MajorRecommendationData(
        total_majors_evaluated=10,
        best_score=26.5,
        best_combination="A00",
        priority_score=0.5,
        safety_tier=st,
        target_tier=st,
        dream_tier=st,
        strategic_advice=["Lời khuyên 1"],
    )
    assert mrd.total_majors_evaluated == 10
    assert len(mrd.strategic_advice) == 1


def test_chat_request_validation():
    req = ChatRequest(message="Học phí ngành CNTT là bao nhiêu?")
    assert req.message == "Học phí ngành CNTT là bao nhiêu?"
    assert req.question == "Học phí ngành CNTT là bao nhiêu?"

    req_alias = ChatRequest(question="Xét tuyển học bạ cần điều kiện gì?")
    assert req_alias.message == "Xét tuyển học bạ cần điều kiện gì?"

    with pytest.raises(ValidationError):
        ChatRequest(message="   ")


def test_knowledge_create_request_aliases():
    kcr = KnowledgeCreateRequest(
        topic="Học bổng",
        question="Có những loại học bổng nào?",
        answer="Trường có học bổng khuyến khích học tập và doanh nghiệp.",
    )
    assert kcr.chu_de == "Học bổng"
    assert kcr.cau_hoi_mau == "Có những loại học bổng nào?"
    assert kcr.noi_dung == "Trường có học bổng khuyến khích học tập và doanh nghiệp."

    with pytest.raises(ValidationError):
        KnowledgeCreateRequest(topic="   ", answer="Nội dung")


def test_knowledge_item_schema_computed_fields():
    item = KnowledgeItemSchema(
        ma_tri_thuc="tri_thuc_01",
        chu_de="Ký túc xá",
        cau_hoi_mau="Ký túc xá ở đâu?",
        noi_dung="Tại số 99 Nguyễn Chí Thanh",
        trang_thai="active",
    )
    assert item.id == "tri_thuc_01"
    assert item.topic == "Ký túc xá"
    assert item.question == "Ký túc xá ở đâu?"
    assert item.answer == "Tại số 99 Nguyễn Chí Thanh"
    assert item.status == "active"


def test_prediction_repository_anchors():
    repo = PredictionRepository()
    assert len(repo.cached_anchors) == 54
    assert "GHA14" in repo.cached_anchors


def test_prediction_repository_fallback_all_predictions():
    repo = PredictionRepository()
    with patch("src.repositories.prediction_repository.get_db_connection", side_effect=Exception("DB unavailable")):
        res = repo.get_all_2026_predictions()
        assert len(res) == 54
        assert any(r["ma_chuong_trinh"] == "GHA14" for r in res)


def test_prediction_repository_fallback_single_major():
    repo = PredictionRepository()
    with patch("src.repositories.prediction_repository.get_db_connection", side_effect=Exception("DB unavailable")):
        item = repo.get_2026_prediction_by_major("GHA14")
        assert item is not None
        assert item["ma_chuong_trinh"] == "GHA14"

        item_none = repo.get_2026_prediction_by_major("NONEXISTENT")
        assert item_none is None


def test_prediction_repository_record_evaluation():
    repo = PredictionRepository()
    for i in range(55):
        repo.record_evaluation({"eval_id": i})
    recent = repo.get_recent_evaluations()
    assert len(recent) == 50
    assert recent[-1]["eval_id"] == 54


def test_major_repository_fallback():
    repo = MajorRepository()
    repo._cache = {
        "7480201": {
            "major_code": "7480201",
            "major_name": "Công nghệ thông tin",
            "faculty": "Khoa CNTT",
            "faculty_code": "KHOI_CN",
            "benchmark_score": 25.85,
            "benchmark_year": 2025,
            "degree_type": "Cử nhân & Kỹ sư tích hợp",
        }
    }
    repo._initialized = True
    assert repo.get_major("7480201")["major_name"] == "Công nghệ thông tin"
    assert len(repo.get_all_majors()) == 1


def test_mbti_repository_fallback_questions():
    repo = MBTIRepository()
    with patch("src.repositories.mbti_repository.get_db_connection", side_effect=Exception("DB down")):
        repo.load_questions()
        assert len(repo.get_questions()) == 20
        assert len(repo.get_question_map()) == 20


def test_chat_repository_fallback_empty_on_exception():
    repo = ChatRepository()
    with patch("src.repositories.chat_repository.get_db_connection", side_effect=Exception("DB down")):
        assert repo.get_active_tri_thuc() == []
        assert repo.get_all_tri_thuc() == []
        assert repo.get_tri_thuc_by_id("id123") is None
        assert repo.create_tri_thuc("chủ đề", "câu hỏi", "nội dung") is None
        assert repo.update_tri_thuc("id123", chu_de="mới") is None
        assert repo.delete_tri_thuc("id123") is False


def test_prediction_service_get_all_predictions():
    items = prediction_service.get_all_predictions()
    assert len(items) == 54
    assert any(i.ma_chuong_trinh == "GHA14" for i in items)


def test_prediction_service_get_prediction_by_major():
    item = prediction_service.get_prediction_by_major("GHA14")
    assert item.ma_chuong_trinh == "GHA14"
    assert item.ten_chuong_trinh == "Công nghệ thông tin"
    assert item.diem_chuan_2025 > 0

    with pytest.raises(NotFoundException):
        prediction_service.get_prediction_by_major("NONEXISTENT_CODE")


def test_prediction_service_simulate_scenario():
    req = BenchmarkScenarioRequest(
        ma_chuong_trinh="GHA14",
        custom_quota_growth=0.05,
        custom_macro_delta=-0.1,
    )
    sim = prediction_service.simulate_scenario(req)
    assert sim.ma_chuong_trinh == "GHA14"
    assert 15.0 <= sim.diem_du_doan_2026 <= 29.5

    with pytest.raises(NotFoundException):
        prediction_service.simulate_scenario(
            BenchmarkScenarioRequest(ma_chuong_trinh="INVALID_CODE")
        )


def test_prediction_service_evaluate_admission_chance():
    req = AdmissionChanceRequest(
        academic_scores={"toan": 9.0, "ly": 8.5, "hoa": 8.5},
        target_major_code="GHA14",
        priority_region="KV1",
    )
    res = prediction_service.evaluate_admission_chance(req)
    assert res.ma_chuong_trinh == "GHA14"
    assert res.tong_diem_xet_tuyen >= 26.0
    assert 0.0 <= res.xac_suat_trung_tuyen <= 100.0


def test_prediction_service_recommend_majors():
    req = AdmissionChanceRequest(
        academic_scores={"toan": 8.0, "ly": 7.5, "hoa": 7.5},
        priority_region="KV3",
    )
    rec = prediction_service.recommend_majors(req)
    assert rec.total_majors_evaluated == 54
    assert rec.safety_tier is not None
    assert rec.target_tier is not None
    assert rec.dream_tier is not None
    assert len(rec.strategic_advice) == 4


def test_mbti_service_get_questions():
    questions = mbti_service.get_questions()
    assert len(questions) in [20, 28]
    assert all(isinstance(q, MBTIQuestion) for q in questions)


def test_mbti_service_process_submission_validation():
    with pytest.raises(ValidationException):
        mbti_service.process_submission(
            MBTISubmitRequest(
                answers=[
                    MBTIAnswerItem(question_id=999, score=5),
                    MBTIAnswerItem(question_id=1, score=4),
                    MBTIAnswerItem(question_id=2, score=3),
                    MBTIAnswerItem(question_id=3, score=2),
                ]
            )
        )

    with pytest.raises(ValidationException):
        mbti_service.process_submission(
            MBTISubmitRequest(
                answers=[
                    MBTIAnswerItem(question_id=1, score=5),
                    MBTIAnswerItem(question_id=1, score=4),
                    MBTIAnswerItem(question_id=2, score=3),
                    MBTIAnswerItem(question_id=3, score=2),
                ]
            )
        )


def test_mbti_service_get_history_validation():
    with pytest.raises(ValidationException):
        mbti_service.get_history()
