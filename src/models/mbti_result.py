from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from pydantic import BaseModel


class MBTIResultRecord(BaseModel):
    ma_ket_qua: str
    cccd: Optional[str] = None
    session_id: str
    nhom_tinh_cach: Optional[str] = None
    goi_y_nganh: Optional[Union[Dict[str, Any], List[Any], str]] = None
    thoi_gian_thuc_hien: Optional[datetime] = None
    create_at: Optional[datetime] = None
