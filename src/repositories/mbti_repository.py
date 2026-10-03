import json
import logging
import uuid
from datetime import datetime
from typing import Any, Dict, List, Optional
from src.core.database import get_db_connection
from src.ml.mbti.scorer import MBTI_QUESTIONS

logger = logging.getLogger(__name__)


class MBTIRepository:
    def __init__(self):
        self._questions_cache: List[Dict[str, Any]] = []
        self._questions_map: Dict[int, Dict[str, Any]] = {}
        self._initialized: bool = False

    def load_questions(self) -> None:
        query = (
            "SELECT id, noi_dung, chieu_do, chieu_tich_cuc, linh_vuc_ngu_canh, trang_thai "
            "FROM cau_hoi_mbti "
            "WHERE trang_thai = 'active' "
            "ORDER BY id ASC;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    rows = cur.fetchall()
                    if rows:
                        new_cache: List[Dict[str, Any]] = []
                        new_map: Dict[int, Dict[str, Any]] = {}
                        for r in rows:
                            q_item = {
                                "id": int(r[0]),
                                "text": str(r[1]),
                                "dimension": str(r[2]),
                                "category": str(r[2]),
                                "positive_trait": str(r[3]),
                                "context_field": str(r[4]) if r[4] else None,
                            }
                            new_cache.append(q_item)
                            new_map[q_item["id"]] = q_item
                        self._questions_cache = new_cache
                        self._questions_map = new_map
                        self._initialized = True
                        logger.info(f"Đã nạp {len(self._questions_cache)} câu hỏi MBTI từ CSDL Supabase vào cache.")
                        return
        except Exception as e:
            logger.error(f"Lỗi khi nạp câu hỏi MBTI từ CSDL: {str(e)}. Sử dụng bộ câu hỏi mặc định.")

        self._questions_cache = list(MBTI_QUESTIONS)
        self._questions_map = {q["id"]: q for q in MBTI_QUESTIONS}
        self._initialized = True

    def get_questions(self) -> List[Dict[str, Any]]:
        if not self._initialized:
            self.load_questions()
        return self._questions_cache

    def get_question_map(self) -> Dict[int, Dict[str, Any]]:
        if not self._initialized:
            self.load_questions()
        return self._questions_map

    def save_result(
        self,
        session_id: str,
        nhom_tinh_cach: str,
        goi_y_nganh: Any,
        cccd: Optional[str] = None,
    ) -> Optional[str]:
        new_id = str(uuid.uuid4())
        query = (
            "INSERT INTO ket_qua_trac_nghiem "
            "(ma_ket_qua, cccd, session_id, nhom_tinh_cach, goi_y_nganh, thoi_gian_thuc_hien, create_at) "
            "VALUES (%s, %s, %s, %s, %s, %s, %s) "
            "RETURNING ma_ket_qua;"
        )
        now = datetime.utcnow()
        goi_y_str = json.dumps(goi_y_nganh, ensure_ascii=False) if not isinstance(goi_y_nganh, str) else goi_y_nganh
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (new_id, cccd, session_id, nhom_tinh_cach, goi_y_str, now, now))
                    conn.commit()
                    return new_id
        except Exception as e:
            logger.error(f"Lỗi khi lưu kết quả trắc nghiệm vào CSDL: {str(e)}")
            return None

    def get_result_by_id(self, ma_ket_qua: str) -> Optional[Dict[str, Any]]:
        query = (
            "SELECT ma_ket_qua, cccd, session_id, nhom_tinh_cach, goi_y_nganh, thoi_gian_thuc_hien, create_at "
            "FROM ket_qua_trac_nghiem "
            "WHERE ma_ket_qua = %s;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (ma_ket_qua,))
                    r = cur.fetchone()
                    if r:
                        goi_y = r[4]
                        if isinstance(goi_y, str):
                            try:
                                goi_y = json.loads(goi_y)
                            except Exception:
                                pass
                        return {
                            "ma_ket_qua": str(r[0]),
                            "cccd": r[1],
                            "session_id": r[2],
                            "nhom_tinh_cach": r[3],
                            "goi_y_nganh": goi_y,
                            "thoi_gian_thuc_hien": str(r[5]) if r[5] else None,
                            "create_at": str(r[6]) if r[6] else None,
                        }
        except Exception as e:
            logger.error(f"Lỗi khi truy vấn kết quả trắc nghiệm {ma_ket_qua}: {str(e)}")
        return None

    def get_history_by_session(self, session_id: str) -> List[Dict[str, Any]]:
        query = (
            "SELECT ma_ket_qua, cccd, session_id, nhom_tinh_cach, goi_y_nganh, thoi_gian_thuc_hien, create_at "
            "FROM ket_qua_trac_nghiem "
            "WHERE session_id = %s "
            "ORDER BY thoi_gian_thuc_hien DESC;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (session_id,))
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        goi_y = r[4]
                        if isinstance(goi_y, str):
                            try:
                                goi_y = json.loads(goi_y)
                            except Exception:
                                pass
                        result.append({
                            "ma_ket_qua": str(r[0]),
                            "cccd": r[1],
                            "session_id": r[2],
                            "nhom_tinh_cach": r[3],
                            "goi_y_nganh": goi_y,
                            "thoi_gian_thuc_hien": str(r[5]) if r[5] else None,
                            "create_at": str(r[6]) if r[6] else None,
                        })
                    return result
        except Exception as e:
            logger.error(f"Lỗi khi lấy lịch sử trắc nghiệm cho session {session_id}: {str(e)}")
            return []


mbti_repository = MBTIRepository()
