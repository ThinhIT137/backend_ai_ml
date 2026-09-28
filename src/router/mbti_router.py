from fastapi import APIRouter, status
from src.schemas.mbti_schema import (
    MBTIQuestionListResponse,
    MBTIResultResponse,
    MBTISubmitRequest,
)
from src.services.mbti_service import mbti_service

router = APIRouter(prefix="/mbti", tags=["MBTI Assessment"])


@router.get(
    "/questions",
    response_model=MBTIQuestionListResponse,
)
async def get_questions():
    questions = mbti_service.get_questions()
    return MBTIQuestionListResponse(
        success=True,
        total=len(questions),
        data=questions,
    )


@router.post(
    "/submit",
    response_model=MBTIResultResponse,
    status_code=status.HTTP_200_OK,
)
async def submit_mbti(request: MBTISubmitRequest):
    result = mbti_service.process_submission(request)
    return MBTIResultResponse(
        success=True,
        data=result,
    )
