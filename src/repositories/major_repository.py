import logging
from typing import Any, Dict, List, Optional
from src.core.database import get_db_connection

logger = logging.getLogger(__name__)


class MajorRepository:
    def __init__(self):
        self._cache: Dict[str, Dict[str, Any]] = {}
        self._initialized: bool = False

    def load_cache(self) -> None:
        query = (
            "WITH latest_scores AS ("
            "    SELECT DISTINCT ON (c.ma_nganh) c.ma_nganh, d.diem, l.nam "
            "    FROM chuong_trinh_dao_tao c "
            "    JOIN lich_su_diem_chuan l ON c.ma_chuong_trinh = l.ma_chuong_trinh "
            "    JOIN diem_trung_tuyen d ON l.ma_ls_dc = d.ma_ls_dc "
            "    WHERE d.ma_phuong_thuc = 'PT1' "
            "    ORDER BY c.ma_nganh, l.nam DESC, d.diem DESC"
            ") "
            "SELECT n.ma_nganh, n.ten_nganh, "
            "       COALESCE(k.ten_khoi_nganh, 'Đại học Giao thông Vận tải') as ten_khoi, "
            "       n.ma_khoi_nganh, ls.diem as diem_chuan_pt1, ls.nam as nam_diem_chuan "
            "FROM nganh_hoc n "
            "LEFT JOIN khoi_nganh k ON n.ma_khoi_nganh = k.ma_khoi_nganh "
            "LEFT JOIN latest_scores ls ON n.ma_nganh = ls.ma_nganh "
            "ORDER BY n.ma_nganh;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    rows = cur.fetchall()
                    new_cache: Dict[str, Dict[str, Any]] = {}
                    for row in rows:
                        ma_nganh = str(row[0]).strip()
                        new_cache[ma_nganh] = {
                            "major_code": ma_nganh,
                            "major_name": row[1],
                            "faculty": row[2],
                            "faculty_code": row[3],
                            "benchmark_score": float(row[4]) if row[4] is not None else None,
                            "benchmark_year": int(row[5]) if row[5] is not None else None,
                            "degree_type": "Cử nhân & Kỹ sư tích hợp",
                        }
                    self._cache = new_cache
                    self._initialized = True
                    logger.info(f"Đã nạp {len(self._cache)} ngành đào tạo từ Supabase vào cache.")
        except Exception as e:
            logger.error(f"Không thể nạp dữ liệu ngành học từ Supabase: {str(e)}")

    def get_major(self, major_code: str) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            self.load_cache()
        return self._cache.get(str(major_code).strip())

    def get_all_majors(self) -> List[Dict[str, Any]]:
        if not self._initialized:
            self.load_cache()
        return list(self._cache.values())


major_repository = MajorRepository()
