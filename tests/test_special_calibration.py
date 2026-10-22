import pytest
from src.services.prediction_service import prediction_service


def test_calibrate_major_cutoff_identity():
    score = prediction_service.calibrate_major_cutoff("GHA14", 24.20)
    assert score == 24.20


def test_calibrate_major_cutoff_quota_expansion():
    score = prediction_service.calibrate_major_cutoff(
        "GHA32", 23.0, quota_change_percent=10.0, macro_exam_delta=0.0
    )
    assert score == 22.85


def test_calibrate_major_cutoff_quota_contraction():
    score = prediction_service.calibrate_major_cutoff(
        "GHA16QT", 23.0, quota_change_percent=-20.0, macro_exam_delta=0.0
    )
    assert score == 23.30


def test_calibrate_major_cutoff_macro_exam_shift():
    score = prediction_service.calibrate_major_cutoff(
        "GHA01", 24.0, quota_change_percent=0.0, macro_exam_delta=-0.80
    )
    assert score == 23.20


def test_calibrate_combined_quota_and_macro():
    score = prediction_service.calibrate_major_cutoff(
        "GHA24", 24.50, quota_change_percent=5.0, macro_exam_delta=0.30
    )
    assert score == 24.73


def test_calibrate_major_cutoff_clamping_bounds():
    assert (
        prediction_service.calibrate_major_cutoff(
            "GHA32", 14.20, quota_change_percent=50.0, macro_exam_delta=-2.0
        )
        == 14.0
    )
    assert (
        prediction_service.calibrate_major_cutoff(
            "GHA10", 29.20, quota_change_percent=-50.0, macro_exam_delta=2.0
        )
        == 29.5
    )
