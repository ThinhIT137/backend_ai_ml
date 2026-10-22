from typing import Any, Dict, List, Optional
from pydantic import BaseModel, ConfigDict, Field, computed_field, field_validator, model_validator


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

    academic_scores: Dict[str, float] = Field(default_factory=dict)
    target_major_code: Optional[str] = None
    admission_method: str = "PT1"
    priority_region: Optional[str] = "KV3"
    priority_group: Optional[str] = None
    foreign_language_cert: Optional[ForeignLanguageCert] = None

    @model_validator(mode="before")
    @classmethod
    def normalize_frontend_payload(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if "target_major_code" not in data and "ma_chuong_trinh" in data:
                data["target_major_code"] = data["ma_chuong_trinh"]
            if "priority_region" not in data and "khu_vuc" in data:
                data["priority_region"] = data["khu_vuc"]
            if not data.get("academic_scores") and "diem_xet_tuyen" in data:
                score = float(data["diem_xet_tuyen"])
                combo = str(data.get("ma_to_hop", "A00")).upper()
                combo_subs = {
                    "A00": ("toan", "vat_ly", "hoa_hoc"),
                    "A01": ("toan", "vat_ly", "tieng_anh"),
                    "B00": ("toan", "hoa_hoc", "sinh_hoc"),
                    "C00": ("ngu_van", "lich_su", "dia_ly"),
                    "C01": ("toan", "ngu_van", "vat_ly"),
                    "D01": ("toan", "ngu_van", "tieng_anh"),
                    "D07": ("toan", "hoa_hoc", "tieng_anh"),
                    "D09": ("toan", "lich_su", "tieng_anh"),
                    "D10": ("toan", "dia_ly", "tieng_anh"),
                    "X06": ("toan", "vat_ly", "tin_hoc"),
                }.get(combo, ("toan", "vat_ly", "hoa_hoc"))
                part = round(score / 3.0, 2)
                last_part = round(score - 2 * part, 2)
                data["academic_scores"] = {
                    combo_subs[0]: part,
                    combo_subs[1]: part,
                    combo_subs[2]: last_part,
                }
        return data

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
    confidence_level: Optional[str] = "HIGH"
    trend_insight: Optional[str] = None

    @computed_field
    def chance_percentage(self) -> float:
        return self.xac_suat_trung_tuyen

    @computed_field
    def evaluation(self) -> str:
        return self.nhan_xet_chuyen_gia


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


class DynamicTimelinePoint(BaseModel):
    day_offset: int
    total_applicants: int
    empirical_cutoff: float
    predicted_cutoff: float
    weight_evidence: float


class NewsArticleItem(BaseModel):
    title: str
    link: Optional[str] = None
    published_date: Optional[str] = None
    source: Optional[str] = None
    sector: str
    sentiment_score: float
    summary: str


class DynamicBenchmarkDetail(BaseModel):
    ma_chuong_trinh: str
    ten_chuong_trinh: str
    chi_tieu: int
    prior_cutoff: float
    current_cutoff: float
    news_impact_delta: float
    confidence_level: str
    timeline: List[DynamicTimelinePoint] = []
    news_insights: List[NewsArticleItem] = []
    analysis_summary: str


class DynamicBenchmarkResponse(BaseModel):
    success: bool = True
    data: DynamicBenchmarkDetail


class NewsFeedResponse(BaseModel):
    success: bool = True
    total: int
    data: List[NewsArticleItem]


class ColdStartMajorRequest(BaseModel):
    ma_chuong_trinh: str
    ten_chuong_trinh: str
    cluster: Optional[str] = None
    faculty: Optional[str] = None
    degree_type: str = "KỸ_SƯ"
    chi_tieu: int = 50
    external_ref_score: Optional[float] = None


class ColdStartNeighbor(BaseModel):
    cluster: str
    benchmark_base: float
    similarity: float
    faculty: str


class ColdStartMajorDetail(BaseModel):
    ma_chuong_trinh: str
    ten_chuong_trinh: str
    cluster: str
    estimated_cutoff: float
    score_range_min: float
    score_range_max: float
    confidence_level: str = "LOW_COLD_START"
    nearest_neighbors: List[ColdStartNeighbor] = []
    recommendations: List[str] = []


class ColdStartMajorResponse(BaseModel):
    success: bool = True
    data: ColdStartMajorDetail


class PercentileEquatingRequest(BaseModel):
    raw_score: float
    source_subject: str = "Tin học"
    target_subject: str = "Toán"


class PercentileEquatingDetail(BaseModel):
    source_subject: str
    raw_score: float
    target_subject: str
    z_score: float
    percentile: float
    equated_score: float


class PercentileEquatingResponse(BaseModel):
    success: bool = True
    data: PercentileEquatingDetail
