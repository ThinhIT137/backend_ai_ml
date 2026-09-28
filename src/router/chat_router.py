from fastapi import APIRouter, status
from src.schemas.chat_schema import (
    ChatRequest,
    ChatResponse,
    KnowledgeListResponse,
    KnowledgeSyncResponse,
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
