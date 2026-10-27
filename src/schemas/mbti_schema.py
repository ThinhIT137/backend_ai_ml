from typing import Any, Dict, List, Literal, Optional, Union
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, field_serializer


class MBTIQuestion(BaseModel):
    id: int = Field(..., description="ID định danh câu hỏi")
    text: str = Field(..., description="Nội dung câu hỏi tình huống định hướng nghề nghiệp")
    dimension: Literal["EI", "SN", "TF", "JP"] = Field(..., description="Trục đánh giá tính cách")
    category: Optional[Literal["EI", "SN", "TF", "JP"]] = Field(
        None, description="Tương thích trực tiếp với interface Question của Frontend"
    )
    positive_trait: Literal["E", "I", "S", "N", "T", "F", "J", "P"] = Field(
        ..., description="Đặc tính tính cách tương ứng với mức đồng ý cao"
    )
    context_field: Optional[str] = Field(
        None, description="Lĩnh vực ngữ cảnh tại UTC (Kỹ thuật, Công nghệ, Xây dựng, Kinh tế...)"
    )

    @computed_field
    def question(self) -> str:
        return self.text

    @computed_field
    def option_a(self) -> Dict[str, str]:
        return {"text": "Đồng ý", "trait": self.positive_trait}

    @computed_field
    def option_b(self) -> Dict[str, str]:
        opposites = {
            "E": "I", "I": "E",
            "S": "N", "N": "S",
            "T": "F", "F": "T",
            "J": "P", "P": "J",
        }
        return {"text": "Không đồng ý", "trait": opposites.get(self.positive_trait, "")}


class MBTIQuestionListResponse(BaseModel):
    success: bool = True
    total: int = Field(..., description="Tổng số câu hỏi")
    data: List[MBTIQuestion] = Field(..., description="Danh sách câu hỏi trắc nghiệm")


class MBTIAnswerItem(BaseModel):
    question_id: int = Field(..., ge=1, description="ID câu hỏi")
    score: int = Field(
        ...,
        ge=1,
        le=5,
        description="Điểm đánh giá: 1 (Hoàn toàn không đồng ý) -> 5 (Hoàn toàn đồng ý)",
    )


class MBTISubmitRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    student_name: Optional[str] = Field(
        default=None, alias="studentName", max_length=100, description="Họ và tên thí sinh (tùy chọn)"
    )
    session_id: Optional[str] = Field(
        default=None, description="Mã phiên làm bài (tương thích cột session_id trong ket_qua_trac_nghiem)"
    )
    cccd: Optional[str] = Field(
        default=None, max_length=20, description="Số CCCD của thí sinh nếu có (tương thích cột cccd)"
    )
    include_ai_advice: bool = Field(
        default=False, description="Tùy chọn tạo lời khuyên định hướng chuyên sâu bằng mô hình AI LLaMA"
    )
    answers: Union[List[MBTIAnswerItem], Dict[Union[int, str], int]] = Field(
        ..., min_length=4, description="Danh sách câu trả lời của thí sinh (hỗ trợ cả Array và Record)"
    )

    @field_validator("answers", mode="before")
    @classmethod
    def normalize_answers(cls, v: Any) -> Any:
        if isinstance(v, dict):
            res = []
            for qid, val in v.items():
                if isinstance(val, str):
                    val_clean = val.strip().upper()
                    if val_clean == "A":
                        score = 5
                    elif val_clean == "B":
                        score = 1
                    else:
                        score = int(val_clean)
                else:
                    score = int(val)
                res.append({"question_id": int(qid), "score": score})
            return res
        return v


class DimensionScore(BaseModel):
    extraversion: float = Field(..., description="% Hướng ngoại (E)")
    introversion: float = Field(..., description="% Hướng nội (I)")
    sensing: float = Field(..., description="% Thực tế / Quan sát (S)")
    intuition: float = Field(..., description="% Trực giác / Tầm nhìn (N)")
    thinking: float = Field(..., description="% Lý tính / Phân tích (T)")
    feeling: float = Field(..., description="% Cảm tính / Đồng cảm (F)")
    judging: float = Field(..., description="% Nguyên tắc / Kế hoạch (J)")
    perceiving: float = Field(..., description="% Linh hoạt / Thích ứng (P)")


class MajorRecommendation(BaseModel):
    major_code: str = Field(..., description="Mã ngành đào tạo chính thức (ví dụ: 7480201)")
    major_name: str = Field(..., description="Tên ngành đào tạo theo Niên giám UTC")
    slug: Optional[str] = Field(None, description="Đường dẫn tĩnh cho router frontend (/tra-cuu-nganh-hoc/:slug)")
    faculty: str = Field(..., description="Khoa/Khối ngành phụ trách đào tạo")
    faculty_code: Optional[str] = Field(None, description="Mã khối ngành từ CSDL (KHOI_CN, KHOI_KT...)")
    degree_type: str = Field(
        default="Cử nhân & Kỹ sư tích hợp",
        description="Hình thức văn bằng (Cử nhân / Kỹ sư tích hợp)",
    )
    match_score: int = Field(
        ..., ge=50, le=100, description="Mức độ tương thích với tính cách (%)"
    )
    reason: str = Field(..., description="Lý do tính cách này phát huy tốt nhất trong ngành")
    benchmark_score: Optional[float] = Field(None, description="Điểm chuẩn THPT mới nhất từ CSDL")
    benchmark_year: Optional[int] = Field(None, description="Năm của điểm chuẩn mới nhất")
    career_prospects: List[str] = Field(
        default_factory=list, description="Vị trí việc làm tiêu biểu sau khi tốt nghiệp"
    )

    @computed_field
    def ma_chuong_trinh(self) -> str:
        return self.major_code

    @computed_field
    def ten_chuong_trinh(self) -> str:
        return self.major_name


class CareerTrajectoryItem(BaseModel):
    phase: str = Field(..., description="Giai đoạn phát triển nghề nghiệp")
    roles: List[str] = Field(..., description="Các vị trí công việc tiêu biểu")
    milestone: str = Field(..., description="Mục tiêu năng lực cốt lõi")


class MBTIResultData(BaseModel):
    result_id: Optional[str] = Field(None, description="Mã kết quả trắc nghiệm trong CSDL ket_qua_trac_nghiem")
    student_name: Optional[str] = Field(None, description="Tên thí sinh")
    session_id: Optional[str] = Field(None, description="Mã phiên làm bài (tương thích Supabase ket_qua_trac_nghiem)")
    cccd: Optional[str] = Field(None, description="CCCD thí sinh")
    mbti_type: str = Field(..., description="Mã nhóm 4 chữ cái (ví dụ: INTJ, ENTP, ISTJ...)")

    type_name: str = Field(..., description="Tên hình tượng (ví dụ: Nhà Kiến thiết Hệ thống)")
    archetype_group: str = Field(
        ..., description="Nhóm khí chất (Nhà Phân tích, Nhà Thực thi, Nhà Thám hiểm, Nhà Ngoại giao)"
    )

    @field_serializer("cccd", when_used="json")
    def serialize_cccd(self, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        cleaned = str(v).strip()
        if len(cleaned) <= 4:
            return "****"
        if len(cleaned) <= 6:
            return f"{cleaned[:2]}***{cleaned[-1:]}"
        return f"{cleaned[:4]}******{cleaned[-2:]}"
    personality_summary: str = Field(..., description="Mô tả tổng quan nét tính cách đặc trưng")
    strengths: List[str] = Field(..., description="Điểm mạnh nổi bật trong tư duy kỹ thuật & làm việc")
    weaknesses: List[str] = Field(default_factory=list, description="Điểm cần lưu ý và rèn luyện thêm")
    work_style: str = Field(..., description="Phong cách học tập & giải quyết vấn đề")
    teamwork_style: Optional[str] = Field(None, description="Phong cách làm việc nhóm đồ án")
    leadership_style: Optional[str] = Field(None, description="Phong cách lãnh đạo & điều phối")
    learning_style: Optional[str] = Field(None, description="Phương pháp học tập tối ưu tại giảng đường đại học")
    suitable_environment: str = Field(
        ..., description="Môi trường học thuật và làm việc lý tưởng tại UTC"
    )
    dimension_scores: DimensionScore = Field(..., description="Điểm phần trăm 4 trục tính cách")
    recommended_majors: List[MajorRecommendation] = Field(
        ..., description="Danh sách các ngành đào tạo UTC phù hợp nhất"
    )
    career_trajectories: List[CareerTrajectoryItem] = Field(
        default_factory=list, description="Bản đồ lộ trình chức danh nghề nghiệp tương lai"
    )
    ai_advice: Optional[str] = Field(None, description="Lời khuyên định hướng chuyên sâu từ chuyên gia AI")

    @computed_field
    def title(self) -> str:
        return self.type_name

    @computed_field
    def description(self) -> str:
        return self.personality_summary

    @computed_field
    def work_environment(self) -> str:
        return self.suitable_environment

    @computed_field
    def scores(self) -> Dict[str, float]:
        return {
            "E": self.dimension_scores.extraversion,
            "I": self.dimension_scores.introversion,
            "S": self.dimension_scores.sensing,
            "N": self.dimension_scores.intuition,
            "T": self.dimension_scores.thinking,
            "F": self.dimension_scores.feeling,
            "J": self.dimension_scores.judging,
            "P": self.dimension_scores.perceiving,
        }


class MBTIResultResponse(BaseModel):
    success: bool = True
    data: MBTIResultData


class MBTIHistoryItem(BaseModel):
    result_id: str = Field(..., description="Mã kết quả trắc nghiệm UUID")
    session_id: str = Field(..., description="Mã phiên trắc nghiệm")
    cccd: Optional[str] = Field(None, description="Số CCCD của thí sinh nếu có")
    mbti_type: str = Field(..., description="Mã nhóm 4 chữ cái MBTI")
    type_name: Optional[str] = Field(None, description="Tên hình tượng tính cách")
    archetype_group: Optional[str] = Field(None, description="Nhóm khí chất")
    thoi_gian_thuc_hien: Optional[str] = Field(None, description="Thời điểm làm trắc nghiệm")
    top_majors: List[str] = Field(default_factory=list, description="Danh sách tên các ngành được gợi ý hàng đầu")

    @field_serializer("cccd", when_used="json")
    def serialize_history_cccd(self, v: Optional[str]) -> Optional[str]:
        if not v:
            return None
        cleaned = str(v).strip()
        if len(cleaned) <= 4:
            return "****"
        if len(cleaned) <= 6:
            return f"{cleaned[:2]}***{cleaned[-1:]}"
        return f"{cleaned[:4]}******{cleaned[-2:]}"


class MBTIHistoryResponse(BaseModel):
    success: bool = True
    total: int = Field(..., description="Tổng số lần làm bài")
    data: List[MBTIHistoryItem] = Field(..., description="Lịch sử các lần trắc nghiệm")


class MBTIDetailResponse(BaseModel):
    success: bool = True
    data: MBTIResultData
