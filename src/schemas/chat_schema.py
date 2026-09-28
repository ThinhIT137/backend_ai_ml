from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, model_validator


class ChatSourceItem(BaseModel):
    doc_label: str = Field(..., description="Tên tài liệu nguồn (Sổ tay K67, Niên giám K64, FAQ Tuyển sinh...)")
    breadcrumb: Optional[str] = Field(None, description="Đường dẫn mục tham chiếu")
    page_range: Optional[str] = Field(None, description="Trang tham chiếu trong tài liệu gốc")
    content_snippet: Optional[str] = Field(None, description="Đoạn trích thông tin liên quan")
    score: Optional[float] = Field(None, description="Điểm tương đồng relevance score")


class ChatRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    message: Optional[str] = Field(None, alias="question", description="Nội dung câu hỏi của người dùng")
    question: Optional[str] = Field(None, description="Tương thích trường question")
    session_id: Optional[str] = Field(None, description="Mã phiên hội thoại (UUID)")
    stream: bool = Field(default=False, description="Tùy chọn streaming SSE (True/False)")

    @model_validator(mode="after")
    def validate_content(self) -> "ChatRequest":
        content = (self.message or self.question or "").strip()
        if not content:
            raise ValueError("Nội dung câu hỏi không được để trống")
        self.message = content
        self.question = content
        return self


class ChatResponseData(BaseModel):
    answer: str = Field(..., description="Câu trả lời đầy đủ từ AI")
    session_id: str = Field(..., description="Mã phiên hội thoại")
    sources: List[ChatSourceItem] = Field(default_factory=list, description="Danh sách tài liệu tham chiếu")
    suggested_questions: List[str] = Field(default_factory=list, description="Gợi ý câu hỏi tiếp theo")


class ChatResponse(BaseModel):
    success: bool = True
    data: ChatResponseData


class KnowledgeItemSchema(BaseModel):
    ma_tri_thuc: Optional[str] = Field(None, description="Mã định danh tri thức")
    chu_de: str = Field(..., description="Chủ đề tri thức")
    cau_hoi_mau: Optional[str] = Field(None, description="Câu hỏi mẫu thường gặp")
    noi_dung: str = Field(..., description="Nội dung thông tin / câu trả lời")
    trang_thai: str = Field(default="active", description="Trạng thái kích hoạt")
    create_at: Optional[str] = Field(None, description="Thời gian tạo")


class KnowledgeListResponse(BaseModel):
    success: bool = True
    total: int = Field(..., description="Tổng số mục tri thức")
    data: List[KnowledgeItemSchema] = Field(..., description="Danh sách tri thức")


class KnowledgeSyncResponse(BaseModel):
    success: bool = True
    total_documents: int = Field(..., description="Tổng số tài liệu và chunks trong chỉ mục RAG")
    supabase_faq_count: int = Field(..., description="Số lượng câu hỏi FAQ nạp từ bảng tri_thuc_ai")
    chunks_count: int = Field(..., description="Số lượng chunks tài liệu đào tạo (Sổ tay & Niên giám)")
    message: str = Field(..., description="Thông báo trạng thái đồng bộ")
