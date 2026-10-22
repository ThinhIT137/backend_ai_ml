import pytest
from src.ml.prediction.cold_start_engine import ColdStartEngine, cold_start_engine


@pytest.fixture
def engine():
    return ColdStartEngine()


def test_normal_cdf(engine):
    assert round(engine._normal_cdf(0.0), 2) == 0.50
    assert engine._normal_cdf(1.0) > 0.8
    assert engine._normal_cdf(-1.0) < 0.2


def test_equate_subject_score_tinhoc(engine):
    res = engine.equate_subject_score(raw_score=8.5, source_subject="Tin học", target_subject="Toán")
    assert res["source_subject"] == "Tin học"
    assert res["target_subject"] == "Toán"
    assert res["z_score"] > 0.0
    assert res["percentile"] > 50.0
    assert 0.0 <= res["equated_score"] <= 10.0


def test_equate_subject_score_bounds(engine):
    low_res = engine.equate_subject_score(raw_score=0.0, source_subject="Tin học", target_subject="Toán")
    assert low_res["equated_score"] >= 0.0

    high_res = engine.equate_subject_score(raw_score=10.0, source_subject="Công nghệ", target_subject="Toán")
    assert high_res["equated_score"] <= 10.0


def test_detect_cluster_by_name(engine):
    assert engine.detect_cluster_by_name("Kỹ thuật Đường sắt Tốc độ cao") == "RAILWAY"
    assert engine.detect_cluster_by_name("Thiết kế Vi mạch Bán dẫn") == "SEMICONDUCTOR"
    assert engine.detect_cluster_by_name("Trí tuệ nhân tạo và Dữ liệu lớn") == "IT_CS"
    assert engine.detect_cluster_by_name("Logistics thông minh") == "LOGISTICS_TRANSPORT"
    assert engine.detect_cluster_by_name("Cầu đường đô thị") == "CIVIL_INFRASTRUCTURE"


def test_estimate_cold_start_major_standalone(engine):
    res = engine.estimate_cold_start_major(
        ma_chuong_trinh="GHA99",
        ten_chuong_trinh="Kỹ thuật Vi mạch Bán dẫn",
        cluster="SEMICONDUCTOR",
        degree_type="KỸ_SƯ",
        chi_tieu=60,
    )
    assert res["ma_chuong_trinh"] == "GHA99"
    assert res["confidence_level"] == "LOW_COLD_START"
    assert 20.0 <= res["estimated_cutoff"] <= 28.0
    assert res["score_range_min"] < res["estimated_cutoff"] < res["score_range_max"]
    assert len(res["nearest_neighbors"]) > 0
    assert len(res["recommendations"]) == 3


def test_estimate_cold_start_major_with_external_ref(engine):
    res = engine.estimate_cold_start_major(
        ma_chuong_trinh="GHA98",
        ten_chuong_trinh="Kỹ thuật Đường sắt Tốc độ cao",
        cluster="RAILWAY",
        external_ref_score=26.0,
    )
    assert res["confidence_level"] == "LOW_COLD_START"
    assert res["estimated_cutoff"] > 22.0
