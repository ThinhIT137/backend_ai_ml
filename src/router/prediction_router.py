from fastapi import APIRouter, status
from src.schemas.prediction_schema import (
    AdmissionChanceRequest,
    AdmissionChanceResponse,
    BenchmarkDetailResponse,
    BenchmarkListResponse,
    BenchmarkScenarioRequest,
    BenchmarkScenarioResponse,
    MajorRecommendationResponse,
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
