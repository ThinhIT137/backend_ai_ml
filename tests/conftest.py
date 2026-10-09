import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from app import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def sample_academic_scores():
    return {
        "toan": 8.6,
        "vat_ly": 8.2,
        "hoa_hoc": 7.8,
        "tieng_anh": 7.0,
        "sinh_hoc": 6.5,
        "ngu_van": 7.5,
    }


@pytest.fixture
def sample_mbti_answers_dict():
    return {
        1: 5, 2: 4, 3: 1, 4: 5, 5: 2,
        6: 4, 7: 5, 8: 4, 9: 5, 10: 4,
        11: 1, 12: 5, 13: 4, 14: 1, 15: 5,
        16: 4, 17: 2, 18: 5, 19: 4, 20: 1,
    }


@pytest.fixture
def sample_mbti_answers_list():
    return [
        {"question_id": 1, "score": 4},
        {"question_id": 2, "score": 5},
        {"question_id": 3, "score": 2},
        {"question_id": 4, "score": 4},
        {"question_id": 5, "score": 1},
        {"question_id": 6, "score": 5},
        {"question_id": 7, "score": 4},
        {"question_id": 8, "score": 3},
        {"question_id": 9, "score": 5},
        {"question_id": 10, "score": 4},
        {"question_id": 11, "score": 2},
        {"question_id": 12, "score": 5},
        {"question_id": 13, "score": 4},
        {"question_id": 14, "score": 1},
        {"question_id": 15, "score": 5},
        {"question_id": 16, "score": 4},
        {"question_id": 17, "score": 3},
        {"question_id": 18, "score": 5},
        {"question_id": 19, "score": 4},
        {"question_id": 20, "score": 2},
    ]
