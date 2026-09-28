from typing import Optional
from fastapi import FastAPI, Header, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.core.exceptions import UnauthorizedException


def setup_cors(app: FastAPI) -> None:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )


async def verify_internal_api_key(
    x_api_key: Optional[str] = Header(None, alias="X-Internal-API-Key"),
) -> bool:
    if not settings.INTERNAL_API_KEY:
        return True

    if not x_api_key or x_api_key != settings.INTERNAL_API_KEY:
        raise UnauthorizedException(message="Khóa API nội bộ không chính xác hoặc bị thiếu")

    return True
