import math
from typing import Dict, List, Optional, Tuple


class AdmissionPredictor:
    def __init__(self):
        self.combinations = {
            "A00": ("toan", "vat_ly", "hoa_hoc"),
            "A01": ("toan", "vat_ly", "tieng_anh"),
            "B00": ("toan", "hoa_hoc", "sinh_hoc"),
            "C00": ("ngu_van", "lich_su", "dia_ly"),
            "C01": ("toan", "ngu_van", "vat_ly"),
            "D01": ("toan", "ngu_van", "tieng_anh"),
            "D07": ("toan", "hoa_hoc", "tieng_anh"),
            "D09": ("toan", "lich_su", "tieng_anh"),
            "D10": ("toan", "dia_ly", "tieng_anh"),
            "X06": ("toan", "vat_ly", "tin_hoc"),
        }
        self.alias_map = {
            "math": "toan",
            "toán": "toan",
            "ly": "vat_ly",
            "vật lý": "vat_ly",
            "physics": "vat_ly",
            "hoa": "hoa_hoc",
            "hóa": "hoa_hoc",
            "hóa học": "hoa_hoc",
            "chemistry": "hoa_hoc",
            "van": "ngu_van",
            "văn": "ngu_van",
            "ngữ văn": "ngu_van",
            "literature": "ngu_van",
            "anh": "tieng_anh",
            "tiếng anh": "tieng_anh",
            "english": "tieng_anh",
            "sinh": "sinh_hoc",
            "sinh học": "sinh_hoc",
            "biology": "sinh_hoc",
            "su": "lich_su",
            "sử": "lich_su",
            "lịch sử": "lich_su",
            "history": "lich_su",
            "dia": "dia_ly",
            "địa": "dia_ly",
            "địa lý": "dia_ly",
            "geography": "dia_ly",
            "tin": "tin_hoc",
            "tin học": "tin_hoc",
            "informatics": "tin_hoc",
        }

    def normalize_scores(self, raw_scores: Dict[str, float]) -> Dict[str, float]:
        norm = {}
        for k, v in raw_scores.items():
            key = k.strip().lower()
            canonical = self.alias_map.get(key, key)
            try:
                norm[canonical] = float(v)
            except (ValueError, TypeError):
                continue
        return norm

    def convert_english_certificate(
        self, cert_type: str, score: float
    ) -> float:
        if not cert_type:
            return 0.0
        t = cert_type.upper().strip()
        if "IELTS" in t:
            if score >= 7.0:
                return 10.0
            if score >= 6.5:
                return 9.5
            if score >= 6.0:
                return 9.0
            if score >= 5.5:
                return 8.5
            if score >= 5.0:
                return 8.0
            return 0.0
        if "TOEFL" in t:
            if score >= 94.0:
                return 10.0
            if score >= 79.0:
                return 9.5
            if score >= 60.0:
                return 9.0
            if score >= 46.0:
                return 8.5
            if score >= 35.0:
                return 8.0
            return 0.0
        if "TOEIC" in t:
            if score >= 850.0:
                return 10.0
            if score >= 785.0:
                return 9.5
            if score >= 700.0:
                return 9.0
            if score >= 600.0:
                return 8.5
            if score >= 500.0:
                return 8.0
            return 0.0
        return 0.0

    def calculate_priority(
        self,
        raw_score: float,
        region: Optional[str] = "KV3",
        group: Optional[str] = None,
    ) -> float:
        r_map = {
            "KV1": 0.75,
            "KV2_NT": 0.50,
            "KV2-NT": 0.50,
            "KV2": 0.25,
            "KV3": 0.00,
        }
        g_map = {
            "UT1": 2.0,
            "DT_01": 2.0,
            "DT1": 2.0,
            "UT2": 1.0,
            "DT_02": 1.0,
            "DT2": 1.0,
        }

        r_key = (region or "KV3").upper().strip()
        g_key = (group or "").upper().strip()

        base_p = r_map.get(r_key, 0.0) + g_map.get(g_key, 0.0)
        if base_p <= 0.0:
            return 0.0

        if raw_score <= 22.5:
            return round(base_p, 2)
        if raw_score >= 30.0:
            return 0.0

        discount = (30.0 - raw_score) / 7.5
        return round(base_p * discount, 2)

    def evaluate_best_combination(
        self,
        scores: Dict[str, float],
        allowed_combos: List[str],
        converted_english: float = 0.0,
    ) -> Tuple[str, float]:
        norm = dict(scores)
        if converted_english > 0:
            current_en = norm.get("tieng_anh", 0.0)
            norm["tieng_anh"] = max(current_en, converted_english)

        combos_to_check = (
            allowed_combos if allowed_combos else list(self.combinations.keys())
        )
        best_combo = combos_to_check[0] if combos_to_check else "A00"
        best_score = 0.0

        for c in combos_to_check:
            if c not in self.combinations:
                continue
            subjs = self.combinations[c]
            if all(s in norm for s in subjs):
                s_total = sum(norm[s] for s in subjs)
                if s_total > best_score:
                    best_score = s_total
                    best_combo = c

        if best_score == 0.0:
            available_values = sorted(norm.values(), reverse=True)
            best_score = (
                sum(available_values[:3]) if len(available_values) >= 3 else 21.0
            )

        return best_combo, round(best_score, 2)

    def calculate_probability(
        self, total_score: float, cutoff: float
    ) -> Tuple[float, float, str]:
        gap = round(total_score - cutoff, 2)
        prob_val = 1.0 / (1.0 + math.exp(-2.2 * gap)) * 100.0
        prob = round(max(2.0, min(99.0, prob_val)), 1)

        if prob >= 85.0:
            level = "RẤT_CAO"
        elif prob >= 65.0:
            level = "CAO"
        elif prob >= 45.0:
            level = "TRUNG_BÌNH"
        else:
            level = "THẤP"

        return gap, prob, level

    def get_advice(
        self, level: str, gap: float, major_name: str
    ) -> str:
        if level == "RẤT_CAO":
            return (
                f"Điểm của bạn vượt trội so với điểm chuẩn dự kiến (+{gap:.2f} điểm). "
                f"Ngành {major_name} là phương án cực kỳ an toàn, có thể đặt làm nguyện vọng 1 hoặc nguyện vọng bảo hiểm."
            )
        if level == "CAO":
            return (
                f"Điểm của bạn nhỉnh hơn điểm chuẩn dự kiến (+{gap:.2f} điểm). "
                f"Ngành {major_name} rất vừa sức, khả năng trúng tuyển lớn, nên đặt ở nhóm nguyện vọng ưu tiên hàng đầu (NV1 - NV3)."
            )
        if level == "TRUNG_BÌNH":
            sign = f"+{gap:.2f}" if gap >= 0 else f"{gap:.2f}"
            return (
                f"Điểm của bạn sát ngưỡng điểm chuẩn dự kiến ({sign} điểm). "
                f"Ngành {major_name} thuộc nhóm mục tiêu có cạnh tranh, nên đặt làm nguyện vọng ước mơ nhưng cần đăng ký thêm ngành an toàn phía sau."
            )
        return (
            f"Điểm của bạn thấp hơn điểm chuẩn dự kiến ({gap:.2f} điểm). "
            f"Xét tuyển vào ngành {major_name} tiềm ẩn rủi ro cao, khuyến nghị bạn nên ưu tiên các ngành cùng nhóm có điểm chuẩn phù hợp hơn."
        )


admission_predictor = AdmissionPredictor()
