import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
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


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info(f"Khởi động {settings.PROJECT_NAME} v{settings.VERSION}...")
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

setup_cors(app)
register_exception_handlers(app)


@app.get("/", tags=["General"])
async def root():
    return {
        "success": True,
        "message": f"Chào mừng đến với {settings.PROJECT_NAME}",
        "docs": "/docs",
        "version": settings.VERSION,
    }


@app.get("/health", tags=["General"])
async def health_check():
    return {
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