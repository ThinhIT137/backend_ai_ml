import pytest
from src.ml.prediction.admission_predictor import (
    AdmissionPredictor,
    admission_predictor,
)


@pytest.fixture
def evaluator():
    return AdmissionPredictor()


def test_normalize_scores_standard_keys(evaluator):
    scores = {"toan": 8.0, "ly": 7.5, "hoa": 8.5}
    norm = evaluator.normalize_scores(scores)
    assert norm["toan"] == 8.0
    assert norm["vat_ly"] == 7.5
    assert norm["hoa_hoc"] == 8.5


def test_normalize_scores_accented_vietnamese(evaluator):
    scores = {"Toán": 9.0, "Vật lý": 8.0, "Hóa học": 8.5, "Tiếng Anh": 7.5}
    norm = evaluator.normalize_scores(scores)
    assert norm["toan"] == 9.0
    assert norm["vat_ly"] == 8.0
    assert norm["hoa_hoc"] == 8.5
    assert norm["tieng_anh"] == 7.5


def test_normalize_scores_english_aliases(evaluator):
    scores = {"math": 8.5, "physics": 9.0, "chemistry": 7.0, "english": 8.0}
    norm = evaluator.normalize_scores(scores)
    assert norm["toan"] == 8.5
    assert norm["vat_ly"] == 9.0
    assert norm["hoa_hoc"] == 7.0
    assert norm["tieng_anh"] == 8.0


def test_convert_english_certificate_ielts_ranges(evaluator):
    assert evaluator.convert_english_certificate("IELTS", 9.0) == 10.0
    assert evaluator.convert_english_certificate("IELTS", 7.5) == 10.0
    assert evaluator.convert_english_certificate("IELTS", 7.0) == 10.0
    assert evaluator.convert_english_certificate("IELTS", 6.5) == 9.5
    assert evaluator.convert_english_certificate("IELTS", 6.0) == 9.0
    assert evaluator.convert_english_certificate("IELTS", 5.5) == 8.5
    assert evaluator.convert_english_certificate("IELTS", 5.0) == 8.0
    assert evaluator.convert_english_certificate("IELTS", 4.5) == 0.0
    assert evaluator.convert_english_certificate("IELTS", 3.0) == 0.0


def test_convert_english_certificate_toefl_ranges(evaluator):
    assert evaluator.convert_english_certificate("TOEFL iBT", 100.0) == 10.0
    assert evaluator.convert_english_certificate("TOEFL iBT", 94.0) == 10.0
    assert evaluator.convert_english_certificate("TOEFL iBT", 80.0) == 9.5
    assert evaluator.convert_english_certificate("TOEFL iBT", 65.0) == 9.0
    assert evaluator.convert_english_certificate("TOEFL iBT", 50.0) == 8.5
    assert evaluator.convert_english_certificate("TOEFL iBT", 38.0) == 8.0
    assert evaluator.convert_english_certificate("TOEFL iBT", 20.0) == 0.0


def test_convert_english_certificate_toeic_ranges(evaluator):
    assert evaluator.convert_english_certificate("TOEIC", 900.0) == 10.0
    assert evaluator.convert_english_certificate("TOEIC", 850.0) == 10.0
    assert evaluator.convert_english_certificate("TOEIC", 790.0) == 9.5
    assert evaluator.convert_english_certificate("TOEIC", 710.0) == 9.0
    assert evaluator.convert_english_certificate("TOEIC", 620.0) == 8.5
    assert evaluator.convert_english_certificate("TOEIC", 520.0) == 8.0
    assert evaluator.convert_english_certificate("TOEIC", 400.0) == 0.0


def test_convert_english_certificate_unknown_type(evaluator):
    assert evaluator.convert_english_certificate("JLPT", 150.0) == 0.0
    assert evaluator.convert_english_certificate("UNKNOWN", 10.0) == 0.0


def test_calculate_priority_kv_base(evaluator):
    assert evaluator.calculate_priority(20.0, region="KV1", group=None) == 0.75
    assert evaluator.calculate_priority(20.0, region="KV2_NT", group=None) == 0.50
    assert evaluator.calculate_priority(20.0, region="KV2-NT", group=None) == 0.50
    assert evaluator.calculate_priority(20.0, region="KV2", group=None) == 0.25
    assert evaluator.calculate_priority(20.0, region="KV3", group=None) == 0.00


def test_calculate_priority_ut_base(evaluator):
    assert evaluator.calculate_priority(20.0, region="KV3", group="UT1") == 2.0
    assert evaluator.calculate_priority(20.0, region="KV3", group="DT_01") == 2.0
    assert evaluator.calculate_priority(20.0, region="KV3", group="UT2") == 1.0
    assert evaluator.calculate_priority(20.0, region="KV3", group="DT_02") == 1.0


def test_calculate_priority_combined_no_discount(evaluator):
    p = evaluator.calculate_priority(21.0, region="KV1", group="UT1")
    assert p == 2.75


def test_calculate_priority_linear_discount_above_22_5(evaluator):
    p_half = evaluator.calculate_priority(26.25, region="KV1", group=None)
    assert p_half == round(0.75 * 0.5, 2)


def test_calculate_priority_at_exact_threshold_22_5(evaluator):
    assert evaluator.calculate_priority(22.5, region="KV1", group=None) == 0.75


def test_calculate_priority_at_max_score_30(evaluator):
    assert evaluator.calculate_priority(30.0, region="KV1", group="UT1") == 0.0


def test_calculate_priority_above_30(evaluator):
    assert evaluator.calculate_priority(31.0, region="KV1", group="UT1") == 0.0


def test_calculate_priority_case_insensitive_and_whitespace(evaluator):
    assert evaluator.calculate_priority(20.0, region=" kv1 ", group=" ut1 ") == 2.75


def test_evaluate_best_combination_a00_vs_a01(evaluator):
    scores = {"toan": 9.0, "vat_ly": 8.0, "hoa_hoc": 7.0, "tieng_anh": 9.0}
    combo, raw = evaluator.evaluate_best_combination(scores, ["A00", "A01"])
    assert combo == "A01"
    assert raw == 26.0


def test_evaluate_best_combination_with_converted_english_boost(evaluator):
    scores = {"toan": 8.0, "vat_ly": 8.0, "tieng_anh": 6.0}
    combo, raw = evaluator.evaluate_best_combination(scores, ["A01"], converted_english=10.0)
    assert combo == "A01"
    assert raw == 26.0


def test_evaluate_best_combination_does_not_downgrade_higher_original_english(evaluator):
    scores = {"toan": 8.0, "vat_ly": 8.0, "tieng_anh": 9.5}
    combo, raw = evaluator.evaluate_best_combination(scores, ["A01"], converted_english=8.0)
    assert raw == 25.5


def test_evaluate_best_combination_all_10_combos_supported(evaluator):
    for c in ["A00", "A01", "B00", "C00", "C01", "D01", "D07", "D09", "D10", "X06"]:
        assert c in evaluator.combinations


def test_evaluate_best_combination_missing_subjects_fallback(evaluator):
    scores = {"toan": 8.0, "vat_ly": 8.0}
    combo, raw = evaluator.evaluate_best_combination(scores, ["B00"])
    assert raw > 0.0


def test_calculate_probability_exact_match(evaluator):
    gap, prob, level = evaluator.calculate_probability(25.0, 25.0)
    assert gap == 0.0
    assert prob == 50.0
    assert level == "TRUNG_BÌNH"


def test_calculate_probability_positive_gap(evaluator):
    gap, prob, level = evaluator.calculate_probability(26.0, 25.0)
    assert gap == 1.0
    assert prob >= 85.0
    assert level == "RẤT_CAO"


def test_calculate_probability_moderate_positive_gap(evaluator):
    gap, prob, level = evaluator.calculate_probability(25.3, 25.0)
    assert gap == 0.3
    assert 60.0 <= prob <= 85.0


def test_calculate_probability_negative_gap(evaluator):
    gap, prob, level = evaluator.calculate_probability(24.0, 25.0)
    assert gap == -1.0
    assert prob <= 20.0
    assert level == "THẤP"


def test_calculate_probability_bounds_clamped(evaluator):
    _, prob_high, _ = evaluator.calculate_probability(35.0, 20.0)
    assert prob_high <= 99.0

    _, prob_low, _ = evaluator.calculate_probability(10.0, 30.0)
    assert prob_low >= 2.0


def test_get_advice_all_levels(evaluator):
    advice_safe = evaluator.get_advice("RẤT_CAO", 1.5, "CNTT")
    assert "rất cao" in advice_safe.lower() or "an toàn" in advice_safe.lower()

    advice_target = evaluator.get_advice("CAO", 0.5, "Logistics")
    assert "triển vọng" in advice_target.lower() or "vừa sức" in advice_target.lower()

    advice_medium = evaluator.get_advice("TRUNG_BÌNH", 0.0, "Co Dien Tu")
    assert "sát ngưỡng" in advice_medium.lower() or "cạnh tranh" in advice_medium.lower()

    advice_low = evaluator.get_advice("THẤP", -1.0, "Tu Dong Hoa")
    assert "rủi ro cao" in advice_low.lower() or "thấp hơn" in advice_low.lower()


def test_singleton_instance():
    assert admission_predictor is not None
    assert isinstance(admission_predictor, AdmissionPredictor)
