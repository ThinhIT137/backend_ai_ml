from typing import Optional
from fastapi import APIRouter, Query, status
from src.schemas.prediction_schema import (
    AdmissionChanceRequest,
    AdmissionChanceResponse,
    BenchmarkDetailResponse,
    BenchmarkListResponse,
    BenchmarkScenarioRequest,
    BenchmarkScenarioResponse,
    ColdStartMajorRequest,
    ColdStartMajorResponse,
    DynamicBenchmarkResponse,
    MajorRecommendationResponse,
    NewsFeedResponse,
    PercentileEquatingRequest,
    PercentileEquatingResponse,
)
from src.services.prediction_service import prediction_service

router = APIRouter(prefix="/predict", tags=["Admission & Benchmark Prediction"])


@router.get(
    "/all-benchmarks",
    response_model=BenchmarkListResponse,
    status_code=status.HTTP_200_OK,
)
async def get_all_benchmarks():
    items = prediction_service.get_all_predictions()
    return BenchmarkListResponse(success=True, total=len(items), data=items)


@router.get(
    "/benchmark/{ma_chuong_trinh}",
    response_model=BenchmarkDetailResponse,
    status_code=status.HTTP_200_OK,
)
async def get_benchmark_by_major(ma_chuong_trinh: str):
    item = prediction_service.get_prediction_by_major(ma_chuong_trinh)
    return BenchmarkDetailResponse(success=True, data=item)


@router.post(
    "/simulate-scenario",
    response_model=BenchmarkScenarioResponse,
    status_code=status.HTTP_200_OK,
)
async def simulate_benchmark_scenario(request: BenchmarkScenarioRequest):
    item = prediction_service.simulate_scenario(request)
    return BenchmarkScenarioResponse(success=True, data=item)


@router.post(
    "/admission-chance",
    response_model=AdmissionChanceResponse,
    status_code=status.HTTP_200_OK,
)
async def evaluate_admission_chance(request: AdmissionChanceRequest):
    result = prediction_service.evaluate_admission_chance(request)
    return AdmissionChanceResponse(success=True, data=result)


@router.post(
    "/recommend-majors",
    response_model=MajorRecommendationResponse,
    status_code=status.HTTP_200_OK,
)
async def recommend_majors(request: AdmissionChanceRequest):
    data = prediction_service.recommend_majors(request)
    return MajorRecommendationResponse(success=True, data=data)


@router.get(
    "/dynamic-trends/{ma_chuong_trinh}",
    response_model=DynamicBenchmarkResponse,
    status_code=status.HTTP_200_OK,
)
async def get_dynamic_trends(
    ma_chuong_trinh: str,
    total_days: int = Query(30, ge=1, le=120),
):
    detail = prediction_service.get_dynamic_trends(
        ma_chuong_trinh, total_days=total_days
    )
    return DynamicBenchmarkResponse(success=True, data=detail)


@router.get(
    "/market-news",
    response_model=NewsFeedResponse,
    status_code=status.HTTP_200_OK,
)
async def get_market_news(sector: Optional[str] = Query(None)):
    items = prediction_service.get_market_news(sector=sector)
    return NewsFeedResponse(success=True, total=len(items), data=items)


@router.post(
    "/cold-start/configure-major",
    response_model=ColdStartMajorResponse,
    status_code=status.HTTP_200_OK,
)
async def configure_cold_start_major(request: ColdStartMajorRequest):
    detail = prediction_service.configure_cold_start_major(request)
    return ColdStartMajorResponse(success=True, data=detail)


@router.post(
    "/cold-start/percentile-equating",
    response_model=PercentileEquatingResponse,
    status_code=status.HTTP_200_OK,
)
async def equate_percentile(request: PercentileEquatingRequest):
    detail = prediction_service.equate_percentile(request)
    return PercentileEquatingResponse(success=True, data=detail)
