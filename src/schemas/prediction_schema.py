from typing import Dict, List, Optional
from pydantic import BaseModel, ConfigDict, field_validator


class EquivalentMethodScores(BaseModel):
    pt1_thpt: float
    pt2_hoc_ba: float
    pt3_hsa: float
    pt4_tsa: float


class BenchmarkPredictionItem(BaseModel):
    ma_chuong_trinh: str
    ten_chuong_trinh: str
    chi_tieu_2025: Optional[int] = None
    chi_tieu_2026: Optional[int] = None
    diem_chuan_2025: float
    diem_du_doan_2026: float
    score_range_min: float
    score_range_max: float
    trend: str
    delta_score: float
    phuong_thuc_quy_doi: EquivalentMethodScores
    to_hop_xet_tuyen: List[str] = []
    influencing_factors: List[str] = []


class BenchmarkDetailResponse(BaseModel):
    success: bool = True
    data: BenchmarkPredictionItem


class BenchmarkListResponse(BaseModel):
    success: bool = True
    total: int
    data: List[BenchmarkPredictionItem]


class BenchmarkScenarioRequest(BaseModel):
    ma_chuong_trinh: str
    custom_quota_growth: Optional[float] = None
    custom_macro_delta: Optional[float] = None


class BenchmarkScenarioResponse(BaseModel):
    success: bool = True
    data: BenchmarkPredictionItem


class ForeignLanguageCert(BaseModel):
    cert_type: str = "IELTS"
    score: float

    @field_validator("score")
    @classmethod
    def validate_cert_score(cls, score: float) -> float:
        if score < 0.0:
            raise ValueError("Điểm chứng chỉ ngoại ngữ không được là số âm")
        return score


class AdmissionChanceRequest(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    academic_scores: Dict[str, float]
    target_major_code: Optional[str] = None
    admission_method: str = "PT1"
    priority_region: Optional[str] = "KV3"
    priority_group: Optional[str] = None
    foreign_language_cert: Optional[ForeignLanguageCert] = None

    @field_validator("academic_scores")
    @classmethod
    def validate_academic_scores(cls, scores: Dict[str, float]) -> Dict[str, float]:
        if not scores:
            raise ValueError("Danh sách điểm môn học không được để trống")
        for subject, score in scores.items():
            if score < 0.0 or score > 10.0:
                raise ValueError(
                    f"Điểm môn '{subject}' không hợp lệ ({score}). Điểm môn học phải nằm trong khoảng từ 0 đến 10"
                )
        return scores


class MajorChanceResult(BaseModel):
    ma_chuong_trinh: str
    ten_chuong_trinh: str
    diem_chuan_du_doan: float
    to_hop_toi_uu: str
    diem_to_hop_goc: float
    diem_uu_tien: float
    tong_diem_xet_tuyen: float
    do_lech_diem: float
    xac_suat_trung_tuyen: float
    muc_do_an_toan: str
    nhan_xet_chuyen_gia: str


class AdmissionChanceResponse(BaseModel):
    success: bool = True
    data: MajorChanceResult


class StrategyTier(BaseModel):
    tier_name: str
    tier_description: str
    recommended_nv_slots: str
    total_majors: int
    majors: List[MajorChanceResult]


class MajorRecommendationData(BaseModel):
    total_majors_evaluated: int
    best_score: float
    best_combination: str
    priority_score: float
    safety_tier: StrategyTier
    target_tier: StrategyTier
    dream_tier: StrategyTier
    strategic_advice: List[str]


class MajorRecommendationResponse(BaseModel):
    success: bool = True
    data: MajorRecommendationData
