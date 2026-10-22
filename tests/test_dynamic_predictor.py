import pytest
from src.ml.prediction.dynamic_predictor import DynamicPredictor, dynamic_predictor


@pytest.fixture
def predictor():
    return DynamicPredictor()


def test_commitment_weights(predictor):
    assert predictor.get_commitment_weight(1) == 1.0
    assert predictor.get_commitment_weight(2) == 0.7
    assert predictor.get_commitment_weight(3) == 0.45
    assert predictor.get_commitment_weight(4) == 0.3
    assert predictor.get_commitment_weight(5) == 0.2
    assert predictor.get_commitment_weight(6) == 0.15
    assert predictor.get_commitment_weight(10) == 0.15


def test_estimate_influx_ratio_monotonic(predictor):
    r_day1 = predictor.estimate_influx_ratio(1, 30)
    r_day15 = predictor.estimate_influx_ratio(15, 30)
    r_day30 = predictor.estimate_influx_ratio(30, 30)

    assert 0.05 <= r_day1 <= 1.0
    assert 0.05 <= r_day15 <= 1.0
    assert 0.05 <= r_day30 <= 1.0
    assert r_day1 < r_day15 < r_day30


def test_filter_and_weight_applications(predictor):
    raw_apps = [
        {"tong_diem": 25.5, "nguyen_vong": 1},
        {"tong_diem": 27.0, "nguyen_vong": 2},
        {"tong_diem": 0.0, "nguyen_vong": 1},
        {"tong_diem": 22.0, "nguyen_vong": 3},
    ]
    weighted = predictor.filter_and_weight_applications(raw_apps)
    assert len(weighted) == 3
    assert weighted[0][0] == 27.0
    assert weighted[0][1] == 0.7
    assert weighted[1][0] == 25.5
    assert weighted[1][1] == 1.0
    assert weighted[2][0] == 22.0


def test_calculate_empirical_cutoff_empty_or_zero_quota(predictor):
    assert predictor.calculate_empirical_cutoff([], 100) == 24.0
    assert predictor.calculate_empirical_cutoff([(25.0, 1.0)], 0) == 24.0


def test_calculate_empirical_cutoff_normal(predictor):
    scores = [
        (28.0, 1.0),
        (27.0, 1.0),
        (26.0, 1.0),
        (25.0, 1.0),
        (24.0, 1.0),
    ]
    cutoff = predictor.calculate_empirical_cutoff(scores, quota=3, influx_ratio=1.0)
    assert cutoff == 26.0


def test_calculate_bayes_dynamic_cutoff(predictor):
    cutoff, w_t = predictor.calculate_bayes_dynamic_cutoff(
        prior_cutoff=25.0,
        empirical_cutoff=27.0,
        applicant_count=100,
        quota=100,
        news_delta=0.5,
    )
    assert 25.0 < cutoff < 28.0
    assert 0.0 < w_t < 1.0


def test_calculate_bayes_dynamic_cutoff_bounds(predictor):
    cutoff, _ = predictor.calculate_bayes_dynamic_cutoff(
        prior_cutoff=10.0,
        empirical_cutoff=8.0,
        applicant_count=1000,
        quota=10,
        news_delta=-5.0,
    )
    assert cutoff >= 14.0

    cutoff_high, _ = predictor.calculate_bayes_dynamic_cutoff(
        prior_cutoff=32.0,
        empirical_cutoff=35.0,
        applicant_count=1000,
        quota=10,
        news_delta=5.0,
    )
    assert cutoff_high <= 30.0


def test_build_trend_timeline_progression(predictor):
    apps = [
        {"day_offset": 1, "tong_diem": 26.5, "nguyen_vong": 1},
        {"day_offset": 5, "tong_diem": 25.0, "nguyen_vong": 2},
        {"day_offset": 10, "tong_diem": 24.0, "nguyen_vong": 1},
    ]
    timeline = predictor.build_trend_timeline(
        prior_cutoff=25.5,
        historical_applications=apps,
        quota=50,
        total_days=10,
        news_delta=0.2,
    )
    assert len(timeline) == 10
    assert timeline[0]["day_offset"] == 1
    assert timeline[-1]["day_offset"] == 10
    assert "predicted_cutoff" in timeline[-1]
    assert "weight_evidence" in timeline[-1]
