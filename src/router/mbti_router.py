from typing import Optional
from fastapi import APIRouter, Depends, status
from src.core.security import get_optional_auth_context
from src.schemas.mbti_schema import (
    MBTIDetailResponse,
    MBTIHistoryResponse,
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


@router.get(
    "/result/{result_id}",
    response_model=MBTIDetailResponse,
    status_code=status.HTTP_200_OK,
)
async def get_mbti_result(
    result_id: str,
    auth_ctx: dict = Depends(get_optional_auth_context),
):
    data = mbti_service.get_result(result_id, mask_pii=not auth_ctx.get("is_authenticated"))
    return MBTIDetailResponse(success=True, data=data)


@router.get(
    "/history",
    response_model=MBTIHistoryResponse,
    status_code=status.HTTP_200_OK,
)
async def get_mbti_history(
    session_id: Optional[str] = None,
    cccd: Optional[str] = None,
    auth_ctx: dict = Depends(get_optional_auth_context),
):
    history = mbti_service.get_history(
        session_id=session_id or auth_ctx.get("session_id"),
        cccd=cccd,
        mask_pii=not auth_ctx.get("is_authenticated"),
    )
    return MBTIHistoryResponse(success=True, total=len(history), data=history)
