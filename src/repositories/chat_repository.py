import logging
import uuid
from typing import Any, Dict, List, Optional
from src.core.database import get_db_connection

logger = logging.getLogger(__name__)


class ChatRepository:
    def get_active_tri_thuc(self) -> List[Dict[str, Any]]:
        query = (
            "SELECT ma_tri_thuc, chu_de, cau_hoi_mau, noi_dung, trang_thai, create_at "
            "FROM tri_thuc_ai "
            "WHERE trang_thai = 'active' "
            "ORDER BY create_at DESC;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        result.append({
                            "ma_tri_thuc": str(r[0]),
                            "chu_de": r[1],
                            "cau_hoi_mau": r[2],
                            "noi_dung": r[3],
                            "trang_thai": r[4],
                            "create_at": str(r[5]) if r[5] else None,
                        })
                    return result
        except Exception as e:
            logger.error(f"Lỗi truy vấn tri_thuc_ai từ Supabase: {str(e)}")
            return []

    def get_all_tri_thuc(self) -> List[Dict[str, Any]]:
        query = (
            "SELECT ma_tri_thuc, chu_de, cau_hoi_mau, noi_dung, trang_thai, create_at "
            "FROM tri_thuc_ai "
            "ORDER BY create_at DESC;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query)
                    rows = cur.fetchall()
                    result = []
                    for r in rows:
                        result.append({
                            "ma_tri_thuc": str(r[0]),
                            "chu_de": r[1],
                            "cau_hoi_mau": r[2],
                            "noi_dung": r[3],
                            "trang_thai": r[4],
                            "create_at": str(r[5]) if r[5] else None,
                        })
                    return result
        except Exception as e:
            logger.error(f"Lỗi lấy toàn bộ tri_thuc_ai từ Supabase: {str(e)}")
            return []

    def create_tri_thuc(
        self,
        chu_de: str,
        cau_hoi_mau: Optional[str],
        noi_dung: str,
        admin_id: str = "00000000-0000-0000-0000-000000000000",
    ) -> Optional[Dict[str, Any]]:
        new_id = str(uuid.uuid4())
        query = (
            "INSERT INTO tri_thuc_ai (ma_tri_thuc, chu_de, cau_hoi_mau, noi_dung, trang_thai, ma_admin_phu_trach) "
            "VALUES (%s, %s, %s, %s, 'active', %s) "
            "RETURNING ma_tri_thuc, chu_de, cau_hoi_mau, noi_dung, trang_thai, create_at;"
        )
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (new_id, chu_de, cau_hoi_mau, noi_dung, admin_id))
                    r = cur.fetchone()
                    conn.commit()
                    if r:
                        return {
                            "ma_tri_thuc": str(r[0]),
                            "chu_de": r[1],
                            "cau_hoi_mau": r[2],
                            "noi_dung": r[3],
                            "trang_thai": r[4],
                            "create_at": str(r[5]) if r[5] else None,
                        }
        except Exception as e:
            logger.error(f"Lỗi tạo bản ghi tri_thuc_ai mới: {str(e)}")
        return None

    def delete_tri_thuc(self, ma_tri_thuc: str) -> bool:
        query = "DELETE FROM tri_thuc_ai WHERE ma_tri_thuc = %s;"
        try:
            with get_db_connection() as conn:
                with conn.cursor() as cur:
                    cur.execute(query, (ma_tri_thuc,))
                    conn.commit()
                    return cur.rowcount > 0
        except Exception as e:
            logger.error(f"Lỗi xóa bản ghi tri_thuc_ai {ma_tri_thuc}: {str(e)}")
            return False


chat_repository = ChatRepository()
