import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.responses import Response
from starlette.middleware.base import BaseHTTPMiddleware
import uvicorn

from src.core.config import settings
from src.core.exceptions import register_exception_handlers
from src.core.security import setup_cors
from src.router.chat_router import router as chat_router
from src.router.mbti_router import router as mbti_router
from src.router.prediction_router import router as prediction_router

logging.basicConfig(
    level=logging.INFO if not settings.DEBUG else logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("admission_ai_ml")


from src.repositories.major_repository import major_repository
from src.services.chat_service import chat_service


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = "default-src 'self'"
        return response

class HeadMethodMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.method == "HEAD":
            request.scope["method"] = "GET"
            response = await call_next(request)
            return Response(
                content=b"",
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type,
            )
        return await call_next(request)


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Khởi động {settings.PROJECT_NAME} v{settings.VERSION}...")
    major_repository.load_cache()
    chat_service.sync_knowledge()
    yield
    logger.info(f"Đang dừng {settings.PROJECT_NAME}...")


app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Microservice Trí tuệ nhân tạo (AI/ML) hỗ trợ tư vấn tuyển sinh, trắc nghiệm MBTI và dự đoán điểm chuẩn UTC.",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(HeadMethodMiddleware)
app.add_middleware(SecurityHeadersMiddleware)
setup_cors(app)
register_exception_handlers(app)


@app.api_route("/", methods=["GET", "HEAD"], tags=["General"])
async def root():
    return {
        "success": True,
        "message": f"Chào mừng đến với {settings.PROJECT_NAME}",
        "docs": "/docs",
        "version": settings.VERSION,
    }


@app.api_route("/api/health", methods=["GET", "HEAD"], tags=["General"])
@app.api_route("/health", methods=["GET", "HEAD"], tags=["General"])
async def health_check():
    return {
        "status": "ok",
        "success": True,
        "data": {
            "status": "healthy",
            "service": settings.PROJECT_NAME,
            "version": settings.VERSION,
        },
    }


app.include_router(mbti_router, prefix=settings.API_PREFIX)
app.include_router(prediction_router, prefix=settings.API_PREFIX)
app.include_router(chat_router, prefix=settings.API_PREFIX)


if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )
