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
                    target_cccd = None
                    if cccd:
                        cur.execute("SELECT 1 FROM thi_sinh WHERE cccd = %s LIMIT 1;", (cccd,))
                        if cur.fetchone():
                            target_cccd = cccd
                    cur.execute(query, (new_id, target_cccd, session_id, nhom_tinh_cach, goi_y_str, now, now))
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
                        raw_payload = r[4]
                        if isinstance(raw_payload, str):
                            try:
                                raw_payload = json.loads(raw_payload)
                            except Exception:
                                raw_payload = {}
                        if isinstance(raw_payload, dict):
                            result = dict(raw_payload)
                            result["result_id"] = str(r[0])
                            result["cccd"] = r[1] or result.get("cccd")
                            result["session_id"] = r[2]
                            result["mbti_type"] = r[3]
                            return result
                        return {
                            "result_id": str(r[0]),
                            "cccd": r[1],
                            "session_id": r[2],
                            "mbti_type": r[3],
                            "recommended_majors": raw_payload if isinstance(raw_payload, list) else [],
                            "type_name": f"Nhóm tính cách {r[3]}",
                            "archetype_group": "Đại học Giao thông Vận tải",
                            "personality_summary": "",
                            "strengths": [],
                            "weaknesses": [],
                            "work_style": "",
                            "suitable_environment": "",
                            "dimension_scores": {
                                "extraversion": 50.0, "introversion": 50.0,
                                "sensing": 50.0, "intuition": 50.0,
                                "thinking": 50.0, "feeling": 50.0,
                                "judging": 50.0, "perceiving": 50.0,
                            },
                        }
        except Exception as e:
            logger.error(f"Lỗi khi truy vấn kết quả trắc nghiệm {ma_ket_qua}: {str(e)}")
        return None

    def get_history(self, session_id: Optional[str] = None, cccd: Optional[str] = None) -> List[Dict[str, Any]]:
        conditions = []
        params = []
        if session_id:
            conditions.append("session_id = %s")
            params.append(session_id)
        if cccd:
            conditions.append("(cccd = %s OR goi_y_nganh::text LIKE %s)")
            params.append(cccd)
            params.append(f'%"{cccd}"%')
        if not conditions:
            return []

        where_clause = " OR ".join(conditions)
        query = (
            f"SELECT ma_ket_qua, cccd, session_id, nhom_tinh_cach, goi_y_nganh, thoi_gian_thuc_hien, create_at "
            f"FROM ket_qua_trac_nghiem "
            f"WHERE {where_clause} "
            f"ORDER BY thoi_gian_thuc_hien DESC;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, tuple(params))
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        raw = r[4]
                        if isinstance(raw, str):
                            try:
                                raw = json.loads(raw)
                            except Exception:
                                raw = {}
                        type_name = raw.get("type_name") if isinstance(raw, dict) else f"Nhóm {r[3]}"
                        archetype_group = raw.get("archetype_group") if isinstance(raw, dict) else None
                        record_cccd = r[1] or (raw.get("cccd") if isinstance(raw, dict) else None)
                        majors = []
                        if isinstance(raw, dict) and "recommended_majors" in raw:
                            majors = [m.get("major_name", "") for m in raw["recommended_majors"][:3]]
                        elif isinstance(raw, list):
                            majors = [m.get("major_name", "") for m in raw[:3]]

                        result.append({
                            "result_id": str(r[0]),
                            "cccd": record_cccd,
                            "session_id": r[2],
                            "mbti_type": r[3],
                            "type_name": type_name,
                            "archetype_group": archetype_group,
                            "thoi_gian_thuc_hien": str(r[5]) if r[5] else None,
                            "top_majors": [m for m in majors if m],
                        })
                    return result
        except Exception as e:
            logger.error(f"Lỗi khi lấy lịch sử trắc nghiệm: {str(e)}")
            return []


mbti_repository = MBTIRepository()
