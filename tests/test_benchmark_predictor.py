import pytest
from src.ml.prediction.benchmark_predictor import (
    BenchmarkPredictor,
    benchmark_predictor,
)


@pytest.fixture
def predictor():
    return BenchmarkPredictor()


def test_benchmark_predictor_assets_loaded(predictor):
    assert len(predictor.anchors) == 54
    assert len(predictor.conversion_data) > 0
    assert predictor.model is not None


def test_benchmark_predictor_anchors_fields(predictor):
    for code, item in predictor.anchors.items():
        assert code.startswith("GHA")
        assert "ten_chuong_trinh" in item
        assert "chi_tieu_2025" in item
        assert "chi_tieu_2026" in item
        assert "diem_chuan_2025_pt1" in item
        assert "to_hop_xet_tuyen" in item
        assert len(item["to_hop_xet_tuyen"]) > 0


def test_determine_cluster_it_cs(predictor):
    for code in ["GHA02", "GHA13", "GHA14", "GHA14QT", "GHA15", "GHA24", "GHA33"]:
        assert predictor.determine_cluster(code) == "IT_CS"


def test_determine_cluster_mechanical(predictor):
    for code in ["GHA16", "GHA16QT", "GHA17", "GHA18", "GHA19", "GHA19DS", "GHA20", "GHA20QT"]:
        assert predictor.determine_cluster(code) == "MECHANICAL_AUTO"


def test_determine_cluster_electrical(predictor):
    for code in ["GHA21", "GHA21DS", "GHA22", "GHA22BD", "GHA22QT", "GHA23", "GHA23DS", "GHA23TM"]:
        assert predictor.determine_cluster(code) == "ELECTRICAL_AUTOMATION"


def test_determine_cluster_economics(predictor):
    for code in ["GHA01", "GHA03", "GHA04", "GHA04QT", "GHA05", "GHA06", "GHA06QT", "GHA07", "GHA08", "GHA08DS", "GHA09", "GHA10", "GHA10QT"]:
        assert predictor.determine_cluster(code) == "ECONOMICS_TRANSPORT"


def test_determine_cluster_default_civil(predictor):
    assert predictor.determine_cluster("GHA99") == "CIVIL_INFRASTRUCTURE"
    assert predictor.determine_cluster("UNKNOWN") == "CIVIL_INFRASTRUCTURE"


def test_determine_trend_positive(predictor):
    assert predictor.determine_trend(0.3) == "TĂNG"
    assert predictor.determine_trend(0.85) == "TĂNG"


def test_determine_trend_negative(predictor):
    assert predictor.determine_trend(-0.3) == "GIẢM"
    assert predictor.determine_trend(-1.2) == "GIẢM"


def test_determine_trend_stable(predictor):
    assert predictor.determine_trend(0.0) == "ỔN_ĐỊNH"
    assert predictor.determine_trend(0.29) == "ỔN_ĐỊNH"
    assert predictor.determine_trend(-0.29) == "ỔN_ĐỊNH"


def test_convert_thpt_to_all_methods_keys(predictor):
    res = predictor.convert_thpt_to_all_methods(25.0)
    assert "pt1_thpt" in res
    assert "pt2_hoc_ba" in res
    assert "pt3_hsa" in res
    assert "pt4_tsa" in res
    assert res["pt1_thpt"] == 25.0


def test_convert_thpt_to_all_methods_bounds(predictor):
    for thpt in [14.0, 18.0, 22.5, 26.0, 30.0]:
        res = predictor.convert_thpt_to_all_methods(thpt)
        assert 14.0 <= res["pt1_thpt"] <= 30.0
        assert 18.0 <= res["pt2_hoc_ba"] <= 30.0
        assert 50.0 <= res["pt3_hsa"] <= 150.0
        assert 35.0 <= res["pt4_tsa"] <= 100.0


def test_convert_thpt_to_all_methods_clipping(predictor):
    res_low = predictor.convert_thpt_to_all_methods(10.0)
    assert res_low["pt1_thpt"] == 14.0

    res_high = predictor.convert_thpt_to_all_methods(35.0)
    assert res_high["pt1_thpt"] == 30.0


def test_get_influencing_factors_railway(predictor):
    factors = predictor.get_influencing_factors("GHA19DS", 0.6)
    assert any("đường sắt" in f.lower() for f in factors)
    assert any("tăng trưởng mạnh" in f.lower() for f in factors)


def test_get_influencing_factors_semiconductor(predictor):
    factors = predictor.get_influencing_factors("GHA22BD", 0.1)
    assert any("bán dẫn" in f.lower() for f in factors)
    assert any("độ ổn định" in f.lower() for f in factors)


def test_get_influencing_factors_english(predictor):
    factors = predictor.get_influencing_factors("GHA01", -0.7)
    assert any("tiếng anh" in f.lower() for f in factors)
    assert any("độ lệch giảm" in f.lower() for f in factors)


def test_get_influencing_factors_logistics(predictor):
    factors = predictor.get_influencing_factors("GHA08", 0.2)
    assert any("chuỗi cung ứng" in f.lower() or "logistics" in f.lower() for f in factors)


def test_predict_scenario_baseline(predictor):
    score = predictor.predict_scenario("GHA14", custom_quota_growth=0.0, custom_macro_delta=0.0)
    anchor_score = predictor.anchors["GHA14"]["diem_chuan_2025_pt1"]
    assert abs(score - anchor_score) < 3.0


def test_predict_scenario_macro_shift(predictor):
    score_normal = predictor.predict_scenario("GHA14", custom_quota_growth=0.0, custom_macro_delta=0.0)
    score_macro_up = predictor.predict_scenario("GHA14", custom_quota_growth=0.0, custom_macro_delta=1.5)
    score_macro_down = predictor.predict_scenario("GHA14", custom_quota_growth=0.0, custom_macro_delta=-1.5)
    assert score_normal != score_macro_up
    assert score_normal != score_macro_down
    assert 15.0 <= score_macro_up <= 29.5
    assert 15.0 <= score_macro_down <= 29.5


def test_predict_scenario_bounds(predictor):
    for code in list(predictor.anchors.keys())[:10]:
        score = predictor.predict_scenario(code)
        assert 15.0 <= score <= 29.5


def test_predict_scenario_unknown_major(predictor):
    score = predictor.predict_scenario("UNKNOWN_999")
    assert score == 24.0


def test_benchmark_predictor_singleton():
    assert benchmark_predictor is not None
    assert isinstance(benchmark_predictor, BenchmarkPredictor)
