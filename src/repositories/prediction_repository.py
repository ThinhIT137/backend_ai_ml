import os
import json
from src.core.database import get_db_connection


class PredictionRepository:
    def __init__(self):
        self.fallback_file = os.path.join(
            os.path.dirname(__file__),
            "..",
            "ml",
            "prediction",
            "assets",
            "hanoi_anchor_2025_2026.json",
        )
        self.cached_anchors = {}
        self.load_fallback_anchors()

    def load_fallback_anchors(self):
        if os.path.exists(self.fallback_file):
            try:
                with open(self.fallback_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.cached_anchors = {
                        item["ma_chuong_trinh_2026"]: item for item in data
                    }
            except Exception:
                self.cached_anchors = {}

    def get_all_2026_predictions(self):
        results = []
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                sql = (
                    "SELECT d.ma_chuong_trinh, c.ten_chuong_trinh, d.diem_du_doan, "
                    "COALESCE(l25.chi_tieu, 60) AS chi_tieu_2025, "
                    "COALESCE(l26.chi_tieu, 60) AS chi_tieu_2026, "
                    "COALESCE(dt25.diem, 23.0) AS diem_chuan_2025 "
                    "FROM du_doan_diem_chuan d "
                    "JOIN chuong_trinh_dao_tao c ON d.ma_chuong_trinh = c.ma_chuong_trinh "
                    "LEFT JOIN lich_su_diem_chuan l25 ON d.ma_chuong_trinh = l25.ma_chuong_trinh AND l25.nam = 2025 "
                    "LEFT JOIN diem_trung_tuyen dt25 ON l25.ma_ls_dc = dt25.ma_ls_dc AND dt25.ma_phuong_thuc = 'PT1' "
                    "LEFT JOIN lich_su_diem_chuan l26 ON d.ma_chuong_trinh = l26.ma_chuong_trinh AND l26.nam = 2026 "
                    "WHERE d.nam_du_doan = 2026 "
                    "ORDER BY d.ma_chuong_trinh;"
                )
                cur.execute(sql)
                rows = cur.fetchall()
                for r in rows:
                    results.append(
                        {
                            "ma_chuong_trinh": r[0],
                            "ten_chuong_trinh": r[1],
                            "diem_du_doan": float(r[2]),
                            "chi_tieu_2025": int(r[3]),
                            "chi_tieu_2026": int(r[4]),
                            "diem_chuan_2025": float(r[5]),
                        }
                    )
        except Exception:
            pass

        if not results and self.cached_anchors:
            for code, item in self.cached_anchors.items():
                c25 = float(item.get("diem_chuan_2025_pt1") or 23.0)
                results.append(
                    {
                        "ma_chuong_trinh": code,
                        "ten_chuong_trinh": item.get("ten_chuong_trinh", ""),
                        "diem_du_doan": c25,
                        "chi_tieu_2025": int(item.get("chi_tieu_2025") or 60),
                        "chi_tieu_2026": int(item.get("chi_tieu_2026") or 60),
                        "diem_chuan_2025": c25,
                    }
                )

        return results

    def get_2026_prediction_by_major(self, ma_chuong_trinh: str):
        try:
            with get_db_connection() as conn:
                cur = conn.cursor()
                sql = (
                    "SELECT d.ma_chuong_trinh, c.ten_chuong_trinh, d.diem_du_doan, "
                    "COALESCE(l25.chi_tieu, 60) AS chi_tieu_2025, "
                    "COALESCE(l26.chi_tieu, 60) AS chi_tieu_2026, "
                    "COALESCE(dt25.diem, 23.0) AS diem_chuan_2025 "
                    "FROM du_doan_diem_chuan d "
                    "JOIN chuong_trinh_dao_tao c ON d.ma_chuong_trinh = c.ma_chuong_trinh "
                    "LEFT JOIN lich_su_diem_chuan l25 ON d.ma_chuong_trinh = l25.ma_chuong_trinh AND l25.nam = 2025 "
                    "LEFT JOIN diem_trung_tuyen dt25 ON l25.ma_ls_dc = dt25.ma_ls_dc AND dt25.ma_phuong_thuc = 'PT1' "
                    "LEFT JOIN lich_su_diem_chuan l26 ON d.ma_chuong_trinh = l26.ma_chuong_trinh AND l26.nam = 2026 "
                    "WHERE d.nam_du_doan = 2026 AND d.ma_chuong_trinh = %s "
                    "LIMIT 1;"
                )
                cur.execute(sql, (ma_chuong_trinh,))
                row = cur.fetchone()
                if row:
                    return {
                        "ma_chuong_trinh": row[0],
                        "ten_chuong_trinh": row[1],
                        "diem_du_doan": float(row[2]),
                        "chi_tieu_2025": int(row[3]),
                        "chi_tieu_2026": int(row[4]),
                        "diem_chuan_2025": float(row[5]),
                    }
        except Exception:
            pass

        if ma_chuong_trinh in self.cached_anchors:
            item = self.cached_anchors[ma_chuong_trinh]
            c25 = float(item.get("diem_chuan_2025_pt1") or 23.0)
            return {
                "ma_chuong_trinh": ma_chuong_trinh,
                "ten_chuong_trinh": item.get("ten_chuong_trinh", ""),
                "diem_du_doan": c25,
                "chi_tieu_2025": int(item.get("chi_tieu_2025") or 60),
                "chi_tieu_2026": int(item.get("chi_tieu_2026") or 60),
                "diem_chuan_2025": c25,
            }

        return None

    def record_evaluation(self, data: dict):
        if not hasattr(self, "_recent_evaluations"):
            self._recent_evaluations = []
        if len(self._recent_evaluations) >= 50:
            self._recent_evaluations.pop(0)
        self._recent_evaluations.append(data)

    def get_recent_evaluations(self):
        if not hasattr(self, "_recent_evaluations"):
            self._recent_evaluations = []
        return list(self._recent_evaluations)


prediction_repository = PredictionRepository()

