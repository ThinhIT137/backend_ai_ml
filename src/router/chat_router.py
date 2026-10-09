from fastapi import APIRouter, Depends, status
from src.core.security import verify_internal_api_key
from src.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    KnowledgeCreateRequest,
    KnowledgeItemSchema,
    KnowledgeListResponse,
    KnowledgeSyncResponse,
    KnowledgeUpdateRequest,
)
from src.services.chat_service import chat_service

router = APIRouter(prefix="/chat", tags=["AI Chatbot Consultation"])


@router.post(
    "",
    response_model=ChatResponse,
    status_code=status.HTTP_200_OK,
)
async def ask_chat(request: ChatRequest):
    result = chat_service.ask(request)
    return ChatResponse(
        success=True,
        data=result,
    )


@router.post(
    "/sync-knowledge",
    response_model=KnowledgeSyncResponse,
    status_code=status.HTTP_200_OK,
)
async def sync_knowledge():
    return chat_service.sync_knowledge()


@router.get(
    "/knowledge",
    response_model=KnowledgeListResponse,
    status_code=status.HTTP_200_OK,
)
async def list_knowledge():
    items = chat_service.get_knowledge_list()
    return KnowledgeListResponse(
        success=True,
        total=len(items),
        data=items,
    )


@router.post(
    "/knowledge",
    response_model=KnowledgeItemSchema,
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(verify_internal_api_key)],
)
async def create_knowledge(request: KnowledgeCreateRequest):
    return chat_service.create_knowledge(request)


@router.put(
    "/knowledge/{ma_tri_thuc}",
    response_model=KnowledgeItemSchema,
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_internal_api_key)],
)
async def update_knowledge(ma_tri_thuc: str, request: KnowledgeUpdateRequest):
    return chat_service.update_knowledge(ma_tri_thuc, request)


@router.delete(
    "/knowledge/{ma_tri_thuc}",
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(verify_internal_api_key)],
)
async def delete_knowledge(ma_tri_thuc: str):
    chat_service.delete_knowledge(ma_tri_thuc)
    return {"success": True, "message": f"Đã xóa thành công mục tri thức {ma_tri_thuc}"}
