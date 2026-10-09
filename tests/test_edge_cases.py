import pytest
from unittest.mock import patch, MagicMock

from src.ml.prediction.admission_predictor import admission_predictor
from src.ml.prediction.benchmark_predictor import benchmark_predictor
from src.ml.mbti.scorer import calculate_mbti_result, MBTI_QUESTIONS
from src.ml.llm.rag import BM25SearchEngine, tokenize_vietnamese, RAGPipeline
from src.ml.llm.prompt_templates import build_rag_prompt, get_default_suggested_questions
from src.core.exceptions import (
    AppException,
    NotFoundException,
    ValidationException,
    ModelInferenceException,
    UnauthorizedException,
)
from src.schemas.prediction_schema import AdmissionChanceRequest, ForeignLanguageCert


def test_priority_exact_threshold_22_5():
    p_below = admission_predictor.calculate_priority(22.0, "KV1", None)
    assert p_below == 0.75

    p_exact = admission_predictor.calculate_priority(22.50, "KV1", None)
    assert p_exact == 0.75

    p_above = admission_predictor.calculate_priority(23.0, "KV1", None)
    assert p_above == 0.70
    assert p_above < 0.75


def test_priority_maximum_score_30_0():
    p_30 = admission_predictor.calculate_priority(30.0, "KV1", "UT1")
    assert p_30 == 0.0


def test_priority_above_maximum_score_35_0():
    p_35 = admission_predictor.calculate_priority(35.0, "KV1", "UT1")
    assert p_35 == 0.0


def test_priority_zero_score():
    p_0 = admission_predictor.calculate_priority(0.0, "KV1", "UT1")
    assert p_0 == 2.75


def test_priority_whitespace_and_casing():
    p1 = admission_predictor.calculate_priority(20.0, " kv1 ", " ut1 ")
    p2 = admission_predictor.calculate_priority(20.0, "KV1", "UT1")
    assert p1 == p2

    p3 = admission_predictor.calculate_priority(20.0, "Kv2-nt", None)
    p4 = admission_predictor.calculate_priority(20.0, "KV2-NT", None)
    assert p3 == p4


def test_priority_invalid_region_and_group():
    p_invalid_reg = admission_predictor.calculate_priority(20.0, "KV99", None)
    assert p_invalid_reg == 0.0

    p_invalid_grp = admission_predictor.calculate_priority(20.0, None, "UT99")
    assert p_invalid_grp == 0.0

    p_none = admission_predictor.calculate_priority(20.0, "NONE", "none")
    assert p_none == 0.0


def test_normalize_scores_extreme_values():
    norm = admission_predictor.normalize_scores({
        "toán": -5.0,
        "vật lý": 15.0,
        "hóa": 8.0,
        "môn_không_xác_định": 9.0,
    })
    assert norm["toan"] == -5.0
    assert norm["vat_ly"] == 15.0
    assert norm["hoa_hoc"] == 8.0
    assert norm["môn_không_xác_định"] == 9.0


def test_convert_english_certificate_ielts_boundaries():
    assert admission_predictor.convert_english_certificate("IELTS", 0.0) == 0.0
    assert admission_predictor.convert_english_certificate("IELTS", 4.5) == 0.0
    assert admission_predictor.convert_english_certificate("IELTS", 5.0) == 8.0
    assert admission_predictor.convert_english_certificate("IELTS", 5.5) == 8.5
    assert admission_predictor.convert_english_certificate("IELTS", 6.0) == 9.0
    assert admission_predictor.convert_english_certificate("IELTS", 6.5) == 9.5
    assert admission_predictor.convert_english_certificate("IELTS", 7.0) == 10.0
    assert admission_predictor.convert_english_certificate("IELTS", 9.0) == 10.0


def test_convert_english_certificate_toefl_boundaries():
    assert admission_predictor.convert_english_certificate("TOEFL", 20.0) == 0.0
    assert admission_predictor.convert_english_certificate("TOEFL", 35.0) == 8.0
    assert admission_predictor.convert_english_certificate("TOEFL", 46.0) == 8.5
    assert admission_predictor.convert_english_certificate("TOEFL", 60.0) == 9.0
    assert admission_predictor.convert_english_certificate("TOEFL", 79.0) == 9.5
    assert admission_predictor.convert_english_certificate("TOEFL", 94.0) == 10.0


def test_convert_english_certificate_toeic_boundaries():
    assert admission_predictor.convert_english_certificate("TOEIC", 400.0) == 0.0
    assert admission_predictor.convert_english_certificate("TOEIC", 500.0) == 8.0
    assert admission_predictor.convert_english_certificate("TOEIC", 600.0) == 8.5
    assert admission_predictor.convert_english_certificate("TOEIC", 700.0) == 9.0
    assert admission_predictor.convert_english_certificate("TOEIC", 785.0) == 9.5
    assert admission_predictor.convert_english_certificate("TOEIC", 850.0) == 10.0


def test_convert_english_certificate_unknown_type():
    assert admission_predictor.convert_english_certificate("CAMBRIDGE", 180.0) == 0.0


def test_evaluate_best_combination_all_zeros():
    norm = {"toan": 0.0, "vat_ly": 0.0, "hoa_hoc": 0.0}
    combo, score = admission_predictor.evaluate_best_combination(norm, ["A00"])
    assert combo == "A00"
    assert score == 0.0


def test_evaluate_best_combination_missing_all():
    norm = {}
    combo, score = admission_predictor.evaluate_best_combination(norm, ["A00", "A01"])
    assert combo == "A00"
    assert score == 21.0


def test_calculate_probability_boundaries():
    gap_large_pos, prob_large_pos, lvl_large_pos = admission_predictor.calculate_probability(28.0, 24.0)
    assert gap_large_pos == 4.0
    assert prob_large_pos == 99.0
    assert lvl_large_pos == "RẤT_CAO"

    gap_zero, prob_zero, lvl_zero = admission_predictor.calculate_probability(24.0, 24.0)
    assert gap_zero == 0.0
    assert prob_zero == 50.0
    assert lvl_zero == "TRUNG_BÌNH"

    gap_large_neg, prob_large_neg, lvl_large_neg = admission_predictor.calculate_probability(18.0, 24.0)
    assert gap_large_neg == -6.0
    assert prob_large_neg == 2.0
    assert lvl_large_neg == "THẤP"


def test_convert_thpt_to_all_methods_extremes():
    res_zero = benchmark_predictor.convert_thpt_to_all_methods(0.0)
    assert res_zero["pt1_thpt"] == 14.0

    res_100 = benchmark_predictor.convert_thpt_to_all_methods(100.0)
    assert res_100["pt1_thpt"] == 30.0


def test_predict_scenario_extreme_parameters():
    score_extreme_pos = benchmark_predictor.predict_scenario(
        "GHA14",
        custom_quota_growth=50.0,
        custom_macro_delta=10.0,
    )
    assert 15.0 <= score_extreme_pos <= 29.5

    score_extreme_neg = benchmark_predictor.predict_scenario(
        "GHA14",
        custom_quota_growth=-50.0,
        custom_macro_delta=-10.0,
    )
    assert 15.0 <= score_extreme_neg <= 29.5


def test_bm25_empty_corpus():
    engine = BM25SearchEngine([])
    assert engine.search("ngành CNTT") == []


def test_bm25_search_scoring():
    chunks = [
        {"chunk_id": "1", "breadcrumb": "Tuyển sinh", "section": "CNTT", "content": "Ngành công nghệ thông tin tuyển sinh 200 chỉ tiêu."},
        {"chunk_id": "2", "breadcrumb": "Đào tạo", "section": "Kinh tế", "content": "Kinh tế vận tải và logistics là thế mạnh của trường."},
    ]
    engine = BM25SearchEngine(chunks)
    res = engine.search("công nghệ thông tin", top_k=2)
    assert len(res) > 0
    assert res[0]["chunk_id"] == "1"
    assert res[0]["score"] > 0.0


def test_tokenize_vietnamese_punctuation():
    text = "Tuyển sinh UTC 2026: ĐHQGHN, ĐHBK! (Cơ sở 1 & Cơ sở 2)"
    tokens = tokenize_vietnamese(text)
    assert "tuyển" in tokens
    assert "utc" in tokens
    assert "2026" in tokens
    assert any("_" in t for t in tokens)


def test_build_rag_prompt_empty_and_multiple_chunks():
    empty_prompt = build_rag_prompt("Học phí là bao nhiêu?", [])
    assert "HỌC PHÍ LÀ BAO NHIÊU?" in empty_prompt or "Học phí là bao nhiêu?" in empty_prompt

    chunks = [
        {"doc_label": "Sổ tay K67", "breadcrumb": "Học phí", "page_range": "Trang 12", "content": "Mức học phí là 400.000đ/tín chỉ."},
        {"doc_label": "Quy chế K65", "breadcrumb": "Học bổng", "page_range": "Trang 5", "content": "Học bổng loại A trị giá 100% học phí."},
    ]
    prompt = build_rag_prompt("Học phí và học bổng?", chunks)
    assert "Sổ tay K67" in prompt
    assert "Quy chế K65" in prompt
    assert "400.000đ/tín chỉ" in prompt


def test_get_default_suggested_questions_categories():
    q_score = get_default_suggested_questions("Điểm chuẩn ngành logistics")
    assert any("điểm chuẩn" in s.lower() for s in q_score)

    q_fee = get_default_suggested_questions("Chi phí học phí đại học")
    assert any("học phí" in s.lower() or "học bổng" in s.lower() for s in q_fee)

    q_major = get_default_suggested_questions("Môn học ngành CNTT")
    assert any("ngành" in s.lower() or "cntt" in s.lower() for s in q_major)

    q_other = get_default_suggested_questions("Thời tiết Hà Nội")
    assert len(q_other) == 4


def test_exception_classes():
    app_exc = AppException("Lỗi ứng dụng", status_code=500, code="APP_ERR")
    assert app_exc.status_code == 500
    assert app_exc.code == "APP_ERR"

    not_found = NotFoundException("Không tìm thấy")
    assert not_found.status_code == 404
    assert not_found.code == "NOT_FOUND"

    val_exc = ValidationException("Sai định dạng")
    assert val_exc.status_code == 422
    assert val_exc.code == "VALIDATION_ERROR"

    inf_exc = ModelInferenceException("Lỗi suy luận")
    assert inf_exc.status_code == 500
    assert inf_exc.code == "MODEL_INFERENCE_ERROR"

    unauth = UnauthorizedException("Chưa xác thực")
    assert unauth.status_code == 401
    assert unauth.code == "UNAUTHORIZED"


def test_mbti_answers_all_extreme_ones():
    answers = {q["id"]: 1 for q in MBTI_QUESTIONS}
    res = calculate_mbti_result(answers)
    assert res.mbti_type in [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP",
    ]
    assert len(res.recommended_majors) > 0


def test_mbti_answers_all_extreme_fives():
    answers = {q["id"]: 5 for q in MBTI_QUESTIONS}
    res = calculate_mbti_result(answers)
    assert res.mbti_type in [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP",
    ]
    assert len(res.recommended_majors) > 0


def test_mbti_answers_string_numeric_keys():
    answers = {str(q["id"]): 3 for q in MBTI_QUESTIONS}
    res = calculate_mbti_result(answers)
    assert res.mbti_type is not None


def test_mbti_career_trajectories_and_advice():
    answers = {q["id"]: 4 for q in MBTI_QUESTIONS}
    res = calculate_mbti_result(answers, include_ai_advice=False)
    assert len(res.career_trajectories) > 0
    assert res.career_trajectories[0].phase is not None
    assert len(res.career_trajectories[0].roles) > 0


def test_foreign_language_cert_no_cert():
    req = AdmissionChanceRequest(
        academic_scores={"toan": 8.5, "ly": 8.0, "hoa": 7.5},
        target_major_code="GHA14",
        foreign_language_cert=None,
    )
    assert req.foreign_language_cert is None
