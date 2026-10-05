from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class ChatHistoryRecord(BaseModel):
    session_id: str
    sender: str
    message: str
    created_at: Optional[datetime] = None
