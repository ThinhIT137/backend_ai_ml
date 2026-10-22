import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


class ColdStartEngine:
    def __init__(self):
        self.subject_distributions = {
            "Toán": {"mean": 6.45, "std": 1.72},
            "Lý": {"mean": 6.67, "std": 1.58},
            "Hóa": {"mean": 6.68, "std": 1.62},
            "Văn": {"mean": 7.23, "std": 1.35},
            "Anh": {"mean": 5.78, "std": 1.95},
            "Tin học": {"mean": 6.80, "std": 1.65},
            "Công nghệ": {"mean": 7.10, "std": 1.50},
        }

        self.cluster_benchmarks = {
            "IT_CS": {
                "base_cutoff": 25.4,
                "keywords": ["công nghệ thông tin", "phần mềm", "khoa học máy tính", "trí tuệ nhân tạo", "ai", "dữ liệu"],
                "faculty": "Công nghệ thông tin",
            },
            "SEMICONDUCTOR": {
                "base_cutoff": 24.8,
                "keywords": ["bán dẫn", "vi mạch", "thiết kế vi mạch", "chip", "điện tử viễn thông"],
                "faculty": "Điện - Điện tử",
            },
            "RAILWAY": {
                "base_cutoff": 23.5,
                "keywords": ["đường sắt", "đường sắt tốc độ cao", "metro", "đầu máy toa xe"],
                "faculty": "Kỹ thuật giao thông",
            },
            "ELECTRONICS_AUTOMATION": {
                "base_cutoff": 24.2,
                "keywords": ["tự động hóa", "cơ điện tử", "điện tử", "robotics", "điều khiển"],
                "faculty": "Điện - Điện tử",
            },
            "MECHANICAL_AUTOMOTIVE": {
                "base_cutoff": 23.8,
                "keywords": ["ô tô", "cơ khí", "chế tạo máy", "động lực"],
                "faculty": "Cơ khí",
            },
            "CIVIL_INFRASTRUCTURE": {
                "base_cutoff": 21.2,
                "keywords": ["cầu đường", "xây dựng", "hạ tầng", "cảng", "thủy lợi", "công trình"],
                "faculty": "Công trình",
            },
            "LOGISTICS_TRANSPORT": {
                "base_cutoff": 24.7,
                "keywords": ["logistics", "chuỗi cung ứng", "quản lý vận tải", "kinh tế vận tải"],
                "faculty": "Vận tải - Kinh tế",
            },
            "ECONOMICS_BUSINESS": {
                "base_cutoff": 24.0,
                "keywords": ["kinh tế", "quản trị kinh doanh", "tài chính", "kế toán"],
                "faculty": "Vận tải - Kinh tế",
            },
        }

    def _normal_cdf(self, z: float) -> float:
        return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))

    def _normal_inverse_cdf(self, p: float) -> float:
        p_clamped = max(1e-6, min(1.0 - 1e-6, p))
        a = [-3.969683028665376e01, 2.209460984245205e02, -2.759285104469687e02, 1.383577518672690e02, -3.066479806614716e01, 2.506628277459239e00]
        b = [-5.447609879822406e01, 1.615858368580409e02, -1.556989798598866e02, 6.680131188771972e01, -1.328068155288572e01]
        c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e00, -2.549732539343734e00, 4.374664141464968e00, 2.938163982698783e00]
        d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e00, 3.754408661907416e00]

        q = p_clamped - 0.5
        if abs(q) <= 0.425:
            r = q * q
            return q * (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) / (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1.0)
        else:
            r = p_clamped if q < 0.0 else 1.0 - p_clamped
            r = math.sqrt(-math.log(r))
            val = (((((c[0] * r + c[1]) * r + c[2]) * r + c[3]) * r + c[4]) * r + c[5]) / ((((d[0] * r + d[1]) * r + d[2]) * r + d[3]) * r + 1.0)
            return -val if q < 0.0 else val

    def equate_subject_score(
        self,
        raw_score: float,
        source_subject: str = "Tin học",
        target_subject: str = "Toán",
    ) -> Dict[str, Any]:
        src_stat = self.subject_distributions.get(source_subject, {"mean": 6.5, "std": 1.6})
        tgt_stat = self.subject_distributions.get(target_subject, {"mean": 6.5, "std": 1.6})

        z = (raw_score - src_stat["mean"]) / max(0.1, src_stat["std"])
        percentile = round(self._normal_cdf(z) * 100.0, 2)
        equated = tgt_stat["mean"] + z * tgt_stat["std"]
        clamped_equated = round(float(np.clip(equated, 0.0, 10.0)), 2)

        return {
            "source_subject": source_subject,
            "raw_score": float(raw_score),
            "target_subject": target_subject,
            "z_score": round(float(z), 3),
            "percentile": percentile,
            "equated_score": clamped_equated,
        }

    def detect_cluster_by_name(self, name: str) -> str:
        clean = name.lower()
        for cluster, info in self.cluster_benchmarks.items():
            for kw in info["keywords"]:
                if kw in clean:
                    return cluster
        return "CIVIL_INFRASTRUCTURE"

    def estimate_cold_start_major(
        self,
        ma_chuong_trinh: str,
        ten_chuong_trinh: str,
        cluster: Optional[str] = None,
        faculty: Optional[str] = None,
        degree_type: str = "KỸ_SƯ",
        chi_tieu: int = 50,
        external_ref_score: Optional[float] = None,
    ) -> Dict[str, Any]:
        matched_cluster = cluster if cluster and cluster in self.cluster_benchmarks else self.detect_cluster_by_name(ten_chuong_trinh)
        cluster_info = self.cluster_benchmarks[matched_cluster]

        base = cluster_info["base_cutoff"]
        if degree_type.upper() == "KỸ_SƯ":
            degree_offset = 0.2
        else:
            degree_offset = -0.1

        quota_effect = -0.05 * (max(20, min(200, chi_tieu)) - 50) / 10.0

        if external_ref_score is not None and external_ref_score > 0.0:
            ref_adjusted = external_ref_score * 0.94
            estimated_cutoff = 0.45 * base + 0.55 * ref_adjusted + degree_offset + quota_effect
        else:
            estimated_cutoff = base + degree_offset + quota_effect

        final_score = round(float(np.clip(estimated_cutoff, 17.0, 28.5)), 2)
        score_min = round(final_score - 1.0, 2)
        score_max = round(final_score + 1.0, 2)

        nearest_neighbors = [
            {
                "cluster": matched_cluster,
                "benchmark_base": base,
                "similarity": 0.92,
                "faculty": cluster_info["faculty"],
            }
        ]

        recommendations = [
            f"Ngành '{ten_chuong_trinh}' là ngành mở mới theo định hướng năm 2027.",
            "Biên độ dự báo được nới rộng ±1.0 điểm do chưa có dữ liệu mỏ neo lịch sử.",
            "Thí sinh nên đăng ký thêm nguyện vọng an toàn thuộc các ngành truyền thống có phổ điểm tương đương.",
        ]

        return {
            "ma_chuong_trinh": ma_chuong_trinh,
            "ten_chuong_trinh": ten_chuong_trinh,
            "cluster": matched_cluster,
            "estimated_cutoff": final_score,
            "score_range_min": score_min,
            "score_range_max": score_max,
            "confidence_level": "LOW_COLD_START",
            "nearest_neighbors": nearest_neighbors,
            "recommendations": recommendations,
        }


cold_start_engine = ColdStartEngine()
