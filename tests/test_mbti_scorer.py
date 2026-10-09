import pytest
from src.ml.mbti.scorer import (
    IN_DEPTH_MBTI_DATA,
    MBTI_PROFILES,
    MBTI_QUESTIONS,
    UTC_MAJORS_DATA,
    calculate_mbti_result,
)
from src.schemas.mbti_schema import MBTIAnswerItem


def test_mbti_questions_total_count():
    assert len(MBTI_QUESTIONS) == 20


def test_mbti_questions_schema_fields():
    for q in MBTI_QUESTIONS:
        assert "id" in q
        assert "text" in q
        assert "dimension" in q
        assert "positive_trait" in q
        assert q["dimension"] in ["EI", "SN", "TF", "JP"]
        assert q["positive_trait"] in ["E", "I", "S", "N", "T", "F", "J", "P"]


def test_mbti_questions_dimension_distribution():
    dims = {"EI": 0, "SN": 0, "TF": 0, "JP": 0}
    for q in MBTI_QUESTIONS:
        dims[q["dimension"]] += 1
    for d, count in dims.items():
        assert count == 5


def test_mbti_profiles_completeness_16_types():
    assert len(MBTI_PROFILES) == 16
    types_list = [
        "INTJ", "INTP", "ENTJ", "ENTP",
        "INFJ", "INFP", "ENFJ", "ENFP",
        "ISTJ", "ISFJ", "ESTJ", "ESFJ",
        "ISTP", "ISFP", "ESTP", "ESFP",
    ]
    for t in types_list:
        assert t in MBTI_PROFILES
        p = MBTI_PROFILES[t]
        assert "type_name" in p
        assert "archetype_group" in p
        assert "summary" in p
        assert "strengths" in p
        assert "work_style" in p
        assert "suitable_environment" in p
        assert "top_majors" in p


def test_in_depth_mbti_data_completeness():
    assert len(IN_DEPTH_MBTI_DATA) == 16
    for t, data in IN_DEPTH_MBTI_DATA.items():
        assert "weaknesses" in data
        assert "teamwork_style" in data
        assert "leadership_style" in data
        assert "learning_style" in data
        assert "career_trajectories" in data


def test_utc_majors_data_not_empty():
    assert len(UTC_MAJORS_DATA) > 0
    for code, m in UTC_MAJORS_DATA.items():
        assert "name" in m
        assert "faculty" in m


def test_calculate_mbti_result_intj_dict_answers():
    answers = {}
    for q in MBTI_QUESTIONS:
        if q["dimension"] == "EI":
            answers[q["id"]] = 1 if q["positive_trait"] == "E" else 5
        elif q["dimension"] == "SN":
            answers[q["id"]] = 1 if q["positive_trait"] == "S" else 5
        elif q["dimension"] == "TF":
            answers[q["id"]] = 5 if q["positive_trait"] == "T" else 1
        elif q["dimension"] == "JP":
            answers[q["id"]] = 5 if q["positive_trait"] == "J" else 1

    res = calculate_mbti_result(answers=answers, student_name="Nguyen Van A", include_ai_advice=False)
    assert res.mbti_type == "INTJ"
    assert res.student_name == "Nguyen Van A"
    assert res.dimension_scores.introversion > res.dimension_scores.extraversion
    assert res.dimension_scores.intuition > res.dimension_scores.sensing
    assert res.dimension_scores.thinking > res.dimension_scores.feeling
    assert res.dimension_scores.judging > res.dimension_scores.perceiving
    assert len(res.recommended_majors) > 0


def test_calculate_mbti_result_esfp_list_answers():
    answers = []
    for q in MBTI_QUESTIONS:
        val = 3
        if q["dimension"] == "EI":
            val = 5 if q["positive_trait"] == "E" else 1
        elif q["dimension"] == "SN":
            val = 5 if q["positive_trait"] == "S" else 1
        elif q["dimension"] == "TF":
            val = 1 if q["positive_trait"] == "T" else 5
        elif q["dimension"] == "JP":
            val = 1 if q["positive_trait"] == "J" else 5
        answers.append(MBTIAnswerItem(question_id=q["id"], score=val))

    res = calculate_mbti_result(answers=answers, include_ai_advice=False)
    assert res.mbti_type == "ESFP"
    assert res.dimension_scores.extraversion > res.dimension_scores.introversion
    assert res.dimension_scores.sensing > res.dimension_scores.intuition
    assert res.dimension_scores.feeling > res.dimension_scores.thinking
    assert res.dimension_scores.perceiving > res.dimension_scores.judging


def test_calculate_mbti_result_entp_answers():
    answers = {}
    for q in MBTI_QUESTIONS:
        if q["dimension"] == "EI":
            answers[q["id"]] = 5 if q["positive_trait"] == "E" else 1
        elif q["dimension"] == "SN":
            answers[q["id"]] = 1 if q["positive_trait"] == "S" else 5
        elif q["dimension"] == "TF":
            answers[q["id"]] = 5 if q["positive_trait"] == "T" else 1
        elif q["dimension"] == "JP":
            answers[q["id"]] = 1 if q["positive_trait"] == "J" else 5

    res = calculate_mbti_result(answers=answers, include_ai_advice=False)
    assert res.mbti_type == "ENTP"


def test_calculate_mbti_result_isfj_answers():
    answers = {}
    for q in MBTI_QUESTIONS:
        if q["dimension"] == "EI":
            answers[q["id"]] = 1 if q["positive_trait"] == "E" else 5
        elif q["dimension"] == "SN":
            answers[q["id"]] = 5 if q["positive_trait"] == "S" else 1
        elif q["dimension"] == "TF":
            answers[q["id"]] = 1 if q["positive_trait"] == "T" else 5
        elif q["dimension"] == "JP":
            answers[q["id"]] = 5 if q["positive_trait"] == "J" else 1

    res = calculate_mbti_result(answers=answers, include_ai_advice=False)
    assert res.mbti_type == "ISFJ"


def test_calculate_mbti_result_neutral_all_3s():
    answers = {i: 3 for i in range(1, 21)}
    res = calculate_mbti_result(answers=answers, include_ai_advice=False)
    assert len(res.mbti_type) == 4
    for dim_score in [
        res.dimension_scores.extraversion,
        res.dimension_scores.introversion,
        res.dimension_scores.sensing,
        res.dimension_scores.intuition,
        res.dimension_scores.thinking,
        res.dimension_scores.feeling,
        res.dimension_scores.judging,
        res.dimension_scores.perceiving,
    ]:
        assert 0.0 <= dim_score <= 100.0


def test_calculate_mbti_result_empty_answers_graceful():
    res = calculate_mbti_result(answers={}, include_ai_advice=False)
    assert len(res.mbti_type) == 4
    assert res.dimension_scores.extraversion == 50.0
    assert res.dimension_scores.introversion == 50.0


def test_calculate_mbti_result_dimension_percentages_sum_to_100():
    for val in [1, 2, 4, 5]:
        answers = {i: val for i in range(1, 21)}
        res = calculate_mbti_result(answers=answers, include_ai_advice=False)
        assert round(res.dimension_scores.extraversion + res.dimension_scores.introversion, 1) == 100.0
        assert round(res.dimension_scores.sensing + res.dimension_scores.intuition, 1) == 100.0
        assert round(res.dimension_scores.thinking + res.dimension_scores.feeling, 1) == 100.0
        assert round(res.dimension_scores.judging + res.dimension_scores.perceiving, 1) == 100.0


def test_calculate_mbti_result_trajectories_present():
    answers = {i: 4 for i in range(1, 21)}
    res = calculate_mbti_result(answers=answers, include_ai_advice=False)
    assert len(res.career_trajectories) > 0
    for traj in res.career_trajectories:
        assert traj.phase is not None
        assert traj.roles is not None


def test_calculate_mbti_result_with_cccd():
    answers = {i: 4 for i in range(1, 21)}
    res = calculate_mbti_result(answers=answers, cccd="001205001234", include_ai_advice=False)
    assert res.cccd == "001205001234"
