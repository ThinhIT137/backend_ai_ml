from typing import List, Optional
from pydantic import BaseModel


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
