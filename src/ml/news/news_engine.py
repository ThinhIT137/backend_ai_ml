import math
import re
import urllib.parse
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple
import xml.etree.ElementTree as ET
import requests

from src.core.config import settings
from src.ml.llm.loader import llm_client


class NewsEngine:
    def __init__(self):
        self.sector_keywords = {
            "IT_CS": [
                "công nghệ thông tin",
                "trí tuệ nhân tạo",
                "lập trình viên",
                "phần mềm",
                "genai",
                "chatgpt",
                "it",
            ],
            "RAILWAY": [
                "đường sắt",
                "đường sắt tốc độ cao",
                "đường sắt đô thị",
                "metro",
                "tàu cao tốc",
            ],
            "CIVIL_CONSTRUCTION": [
                "xây dựng",
                "cầu đường",
                "hạ tầng giao thông",
                "cao tốc",
                "sân bay long thành",
                "công trình",
            ],
            "SEMICONDUCTOR": [
                "bán dẫn",
                "vi mạch",
                "chip",
                "thiết kế vi mạch",
                "bán dẫn việt nam",
            ],
            "LOGISTICS": [
                "logistics",
                "chuỗi cung ứng",
                "vận tải",
                "cảng biển",
                "kho vận",
            ],
            "ECONOMICS": [
                "kinh tế",
                "tài chính",
                "ngân hàng",
                "kế toán",
                "thương mại",
            ],
            "ENGLISH": [
                "tiếng anh",
                "ngôn ngữ anh",
                "ielts",
                "chuẩn đầu ra ngoại ngữ",
            ],
        }

        self.whitelist_keywords = [
            "tuyển sinh",
            "điểm chuẩn",
            "việc làm",
            "nhân lực",
            "kỹ sư",
            "lương",
            "đào tạo",
            "đại học",
            "tuyển dụng",
            "sa thải",
            "đầu tư",
            "công nghệ",
            "thị trường",
        ]

    def passes_whitelist(self, title: str, description: str = "") -> bool:
        combined = f"{title} {description}".lower()
        matched = 0
        for kw in self.whitelist_keywords:
            if kw in combined:
                matched += 1
                if matched >= 1:
                    return True
        return False

    def map_sector_heuristic(self, text: str) -> str:
        clean = text.lower()
        for sector, kws in self.sector_keywords.items():
            for kw in kws:
                if kw in clean:
                    return sector
        return "GENERAL"

    def estimate_sentiment_heuristic(self, text: str) -> float:
        clean = text.lower()
        positives = [
            "tăng",
            "bùng nổ",
            "khát nhân lực",
            "cần tuyển",
            "thu nhập cao",
            "ưu đãi",
            "phê duyệt",
            "đầu tư lớn",
            "cơ hội",
            "phát triển",
            "cam kết việc làm",
        ]
        negatives = [
            "giảm",
            "sa thải",
            "khó xin việc",
            "thắt chặt",
            "thay thế",
            "lo ngại",
            "bão hòa",
            "suy giảm",
            "thất nghiệp",
            "đóng băng",
        ]

        pos_count = sum(1 for p in positives if p in clean)
        neg_count = sum(1 for n in negatives if n in clean)

        diff = pos_count - neg_count
        if diff > 0:
            return round(min(1.0, 0.3 * diff), 2)
        if diff < 0:
            return round(max(-1.0, 0.3 * diff), 2)
        return 0.0

    def parse_google_news_rss(
        self, query: str, max_items: int = 5
    ) -> List[Dict[str, Any]]:
        encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=vi&gl=VN&ceid=VN:vi"
        articles = []
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                root = ET.fromstring(resp.content)
                for item in root.findall(".//item")[:max_items]:
                    title_elem = item.find("title")
                    link_elem = item.find("link")
                    date_elem = item.find("pubDate")
                    source_elem = item.find("source")

                    title = title_elem.text if title_elem is not None else ""
                    link = link_elem.text if link_elem is not None else ""
                    pub_date = date_elem.text if date_elem is not None else ""
                    source = (
                        source_elem.text if source_elem is not None else "Google News"
                    )

                    if self.passes_whitelist(title):
                        sector = self.map_sector_heuristic(title)
                        sentiment = self.estimate_sentiment_heuristic(title)
                        articles.append(
                            {
                                "title": title,
                                "link": link,
                                "published_date": pub_date,
                                "source": source,
                                "sector": sector,
                                "sentiment_score": sentiment,
                                "summary": f"Tin tức về {sector}: {title}",
                            }
                        )
        except Exception:
            pass
        return articles

    def analyze_news_sentiment_with_llm(
        self, title: str, description: str = ""
    ) -> Dict[str, Any]:
        prompt = (
            f"Phân tích tác động của bài báo sau đến tuyển sinh và điểm chuẩn ngành học UTC.\n"
            f"Tiêu đề: {title}\n"
            f"Tóm tắt: {description}\n"
            f"Trả về kết quả dưới định dạng JSON duy nhất gồm:\n"
            f'{{"sector": "IT_CS|RAILWAY|CIVIL_CONSTRUCTION|SEMICONDUCTOR|ECONOMICS|LOGISTICS|ENGLISH|GENERAL", '
            f'"sentiment_score": float từ -1.0 đến 1.0, '
            f'"reason": "giải thích ngắn gọn dưới 30 từ"}}'
        )

        try:
            response = llm_client.generate(
                messages=[
                    {
                        "role": "system",
                        "content": "Bạn là chuyên gia kinh tế giáo dục phân tích tác động thị trường lao động. Trả về đúng định dạng JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=0.2,
                max_tokens=200,
            )
            raw = response.get("choices", [{}])[0].get("message", {}).get("content", "")
            match = re.search(r"\{.*\}", raw, re.DOTALL)
            if match:
                import json
                data = json.loads(match.group(0))
                return {
                    "sector": data.get("sector", self.map_sector_heuristic(title)),
                    "sentiment_score": float(
                        data.get(
                            "sentiment_score", self.estimate_sentiment_heuristic(title)
                        )
                    ),
                    "reason": data.get("reason", title),
                }
        except Exception:
            pass

        return {
            "sector": self.map_sector_heuristic(title),
            "sentiment_score": self.estimate_sentiment_heuristic(title),
            "reason": f"Dựa trên phân tích từ khóa bài viết '{title}'",
        }

    def compute_sector_trend_delta(
        self,
        articles: List[Dict[str, Any]],
        target_sector: str,
        decay_lambda: float = 0.05,
    ) -> Tuple[float, List[Dict[str, Any]]]:
        relevant = [
            a
            for a in articles
            if a.get("sector") == target_sector or a.get("sector") == "GENERAL"
        ]
        if not relevant:
            return 0.0, []

        total_weighted_sentiment = 0.0
        total_weight = 0.0
        insights = []

        for idx, art in enumerate(relevant):
            weight = math.exp(-decay_lambda * idx)
            score = float(art.get("sentiment_score", 0.0))
            total_weighted_sentiment += score * weight
            total_weight += weight
            insights.append(art)

        delta = (
            total_weighted_sentiment / max(0.01, total_weight)
            if total_weight > 0
            else 0.0
        )
        bounded_delta = round(float(min(1.0, max(-1.0, delta))), 2)

        return bounded_delta, insights


news_engine = NewsEngine()
