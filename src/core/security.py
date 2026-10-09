from typing import Optional
from fastapi import FastAPI, Header
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
    authorization: Optional[str] = Header(None, alias="Authorization"),
    x_internal_api_key: Optional[str] = Header(None, alias="X-Internal-API-Key"),
    x_api_key: Optional[str] = Header(None, alias="X-API-Key"),
) -> bool:
    token = None
    if authorization:
        parts = authorization.strip().split()
        if len(parts) == 2 and parts[0].lower() in ["bearer", "token"]:
            token = parts[1]
        else:
            token = authorization.strip()
    elif x_internal_api_key:
        token = x_internal_api_key.strip()
    elif x_api_key:
        token = x_api_key.strip()

    if not token:
        raise UnauthorizedException(message="Yêu cầu xác thực: Thiếu token hoặc API key")

    if settings.INTERNAL_API_KEY and token != settings.INTERNAL_API_KEY:
        raise UnauthorizedException(message="Khóa API hoặc token xác thực không chính xác")

    return True
