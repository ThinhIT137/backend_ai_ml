from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field, model_validator


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
    model_config = ConfigDict(populate_by_name=True)

    ma_tri_thuc: Optional[str] = Field(None, description="Mã định danh tri thức")
    chu_de: str = Field(..., description="Chủ đề tri thức")
    cau_hoi_mau: Optional[str] = Field(None, description="Câu hỏi mẫu thường gặp")
    noi_dung: str = Field(..., description="Nội dung thông tin / câu trả lời")
    trang_thai: str = Field(default="active", description="Trạng thái kích hoạt")
    create_at: Optional[str] = Field(None, description="Thời gian tạo")

    @computed_field
    def id(self) -> Optional[str]:
        return self.ma_tri_thuc

    @computed_field
    def topic(self) -> str:
        return self.chu_de

    @computed_field
    def question(self) -> Optional[str]:
        return self.cau_hoi_mau

    @computed_field
    def answer(self) -> str:
        return self.noi_dung

    @computed_field
    def status(self) -> str:
        return self.trang_thai


class KnowledgeCreateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chu_de: Optional[str] = Field(None, alias="topic")
    cau_hoi_mau: Optional[str] = Field(None, alias="question")
    noi_dung: Optional[str] = Field(None, alias="answer")
    trang_thai: str = Field(default="active", alias="status")
    ma_admin_phu_trach: str = "00000000-0000-0000-0000-000000000000"

    @model_validator(mode="before")
    @classmethod
    def pre_validate(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "topic" in data and "chu_de" not in data:
                data["chu_de"] = data["topic"]
            if "question" in data and "cau_hoi_mau" not in data:
                data["cau_hoi_mau"] = data["question"]
            if "answer" in data and "noi_dung" not in data:
                data["noi_dung"] = data["answer"]
            if "status" in data and "trang_thai" not in data:
                data["trang_thai"] = data["status"]
        return data

    @model_validator(mode="after")
    def validate_fields(self) -> "KnowledgeCreateRequest":
        topic_val = (self.chu_de or "").strip()
        ans_val = (self.noi_dung or "").strip()
        if not topic_val:
            raise ValueError("Chủ đề tri thức (topic/chu_de) không được để trống")
        if not ans_val:
            raise ValueError("Nội dung thông tin (answer/noi_dung) không được để trống")
        self.chu_de = topic_val
        self.noi_dung = ans_val
        return self


class KnowledgeUpdateRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    chu_de: Optional[str] = Field(None, alias="topic")
    cau_hoi_mau: Optional[str] = Field(None, alias="question")
    noi_dung: Optional[str] = Field(None, alias="answer")
    trang_thai: Optional[str] = Field(None, alias="status")

    @model_validator(mode="before")
    @classmethod
    def pre_validate(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "topic" in data and "chu_de" not in data:
                data["chu_de"] = data["topic"]
            if "question" in data and "cau_hoi_mau" not in data:
                data["cau_hoi_mau"] = data["question"]
            if "answer" in data and "noi_dung" not in data:
                data["noi_dung"] = data["answer"]
            if "status" in data and "trang_thai" not in data:
                data["trang_thai"] = data["status"]
        return data


class KnowledgeListResponse(BaseModel):
    success: bool = True
    total: int = Field(..., description="Tổng số mục tri thức")
    data: List[KnowledgeItemSchema] = Field(..., description="Danh sách tri thức")


class KnowledgeSyncResponse(BaseModel):
    success: bool = True
    total_documents: int = Field(..., description="Tổng số tài liệu và chunks trong chỉ mục RAG")
    supabase_faq_count: int = Field(..., description="Số lượng câu hỏi FAQ nạp từ bảng tri_thuc_ai")
    chunks_count: int = Field(default=0, description="Số lượng chunks tài liệu đào tạo (Sổ tay & Niên giám)")
    message: str = Field(..., description="Thông báo trạng thái đồng bộ")
