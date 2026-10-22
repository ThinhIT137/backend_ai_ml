import pytest
from unittest.mock import MagicMock, patch
from src.ml.news.news_engine import NewsEngine, news_engine


@pytest.fixture
def engine():
    return NewsEngine()


def test_whitelist_filter_matches(engine):
    assert engine.passes_whitelist("Thông tin tuyển sinh đại học 2026") is True
    assert engine.passes_whitelist("Nhu cầu kỹ sư phần mềm tăng cao") is True
    assert engine.passes_whitelist("Mức lương trung bình ngành bán dẫn") is True


def test_whitelist_filter_rejects_irrelevant(engine):
    assert engine.passes_whitelist("Bí quyết làm bánh chuối nướng thơm ngon") is False
    assert engine.passes_whitelist("Kết quả trận đấu bóng đá ngoại hạng") is False


def test_map_sector_heuristic(engine):
    assert engine.map_sector_heuristic("Lập trình viên và trí tuệ nhân tạo") == "IT_CS"
    assert engine.map_sector_heuristic("Dự án đường sắt tốc độ cao") == "RAILWAY"
    assert engine.map_sector_heuristic("Thiết kế vi mạch và chip bán dẫn") == "SEMICONDUCTOR"
    assert engine.map_sector_heuristic("Xây dựng cầu đường và hạ tầng cao tốc") == "CIVIL_CONSTRUCTION"
    assert engine.map_sector_heuristic("Quản lý chuỗi cung ứng và logistics") == "LOGISTICS"
    assert engine.map_sector_heuristic("Tài chính ngân hàng và thương mại") == "ECONOMICS"
    assert engine.map_sector_heuristic("Chuẩn đầu ra tiếng anh ielts") == "ENGLISH"
    assert engine.map_sector_heuristic("Thông báo chung của nhà trường") == "GENERAL"


def test_estimate_sentiment_heuristic(engine):
    pos_score = engine.estimate_sentiment_heuristic("Nhu cầu nhân lực bùng nổ, tăng mạnh cơ hội phát triển")
    assert pos_score > 0.0

    neg_score = engine.estimate_sentiment_heuristic("Làn sóng sa thải gia tăng, suy giảm việc làm và lo ngại thất nghiệp")
    assert neg_score < 0.0

    neutral_score = engine.estimate_sentiment_heuristic("Quy trình kiểm tra hồ sơ dự thi")
    assert neutral_score == 0.0


def test_compute_sector_trend_delta(engine):
    articles = [
        {"sector": "IT_CS", "sentiment_score": 0.8},
        {"sector": "IT_CS", "sentiment_score": 0.6},
        {"sector": "GENERAL", "sentiment_score": 0.2},
    ]
    delta, insights = engine.compute_sector_trend_delta(articles, "IT_CS")
    assert delta > 0.0
    assert len(insights) == 3


def test_compute_sector_trend_delta_empty(engine):
    delta, insights = engine.compute_sector_trend_delta([], "RAILWAY")
    assert delta == 0.0
    assert insights == []


def test_analyze_news_sentiment_with_llm_fallback(engine):
    with patch("src.ml.news.news_engine.llm_client.generate", side_effect=Exception("API offline")):
        res = engine.analyze_news_sentiment_with_llm("Nhu cầu kỹ sư bán dẫn tăng vọt")
        assert res["sector"] == "SEMICONDUCTOR"
        assert res["sentiment_score"] > 0.0
        assert "bán dẫn" in res["reason"]


def test_analyze_news_sentiment_with_llm_success(engine):
    mock_resp = {
        "choices": [
            {
                "message": {
                    "content": '{"sector": "IT_CS", "sentiment_score": 0.5, "reason": "Nhu cầu AI tăng cao"}'
                }
            }
        ]
    }
    with patch("src.ml.news.news_engine.llm_client.generate", return_value=mock_resp):
        res = engine.analyze_news_sentiment_with_llm("Phát triển ứng dụng AI")
        assert res["sector"] == "IT_CS"
        assert res["sentiment_score"] == 0.5
        assert res["reason"] == "Nhu cầu AI tăng cao"
