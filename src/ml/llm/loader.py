import logging
from typing import Any, AsyncGenerator, Dict, List, Optional
import httpx
import requests

from src.core.config import settings
from src.core.exceptions import ModelInferenceException

logger = logging.getLogger(__name__)


class NvidiaLLMClient:
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        default_model: Optional[str] = None,
    ):
        self.api_key = api_key or settings.NVIDIA_API_KEY
        self.base_url = base_url or settings.NVIDIA_BASE_URL
        self.default_model = default_model or settings.NVIDIA_MODEL

        if not self.api_key:
            logger.warning(
                "NVIDIA_API_KEY chưa được cấu hình trong .env. Các lệnh gọi LLM sẽ báo lỗi nếu không được cung cấp."
            )

    def _get_headers(self, stream: bool = False) -> Dict[str, str]:
        if not self.api_key:
            raise ModelInferenceException(
                message="Chưa cấu hình NVIDIA_API_KEY trong file .env",
                details={"tip": "Vui lòng thêm NVIDIA_API_KEY vào .env"},
            )
        return {
            "Authorization": f"Bearer {self.api_key}",
            "Accept": "text/event-stream" if stream else "application/json",
            "Content-Type": "application/json",
        }

    def generate(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
        stream: bool = False,
    ) -> Dict[str, Any]:
        headers = self._get_headers(stream=stream)
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature if temperature is not None else settings.LLM_TEMPERATURE,
            "top_p": top_p if top_p is not None else settings.LLM_TOP_P,
            "max_tokens": max_tokens or settings.LLM_MAX_TOKENS,
            "stream": stream,
        }

        try:
            response = requests.post(
                self.base_url,
                headers=headers,
                json=payload,
                stream=stream,
                timeout=60,
            )

            if response.status_code != 200:
                logger.error(f"NVIDIA API Error ({response.status_code}): {response.text}")
                raise ModelInferenceException(
                    message=f"Lỗi phản hồi từ NVIDIA API (Mã lỗi {response.status_code})",
                    details={"response": response.text},
                )

            return response.json()
        except requests.RequestException as e:
            logger.error(f"NVIDIA API Request failed: {str(e)}")
            raise ModelInferenceException(
                message=f"Không thể kết nối đến NVIDIA API: {str(e)}"
            )

    async def generate_async(
        self,
        messages: List[Dict[str, Any]],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        top_p: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        headers = self._get_headers(stream=False)
        payload = {
            "model": model or self.default_model,
            "messages": messages,
            "temperature": temperature if temperature is not None else settings.LLM_TEMPERATURE,
            "top_p": top_p if top_p is not None else settings.LLM_TOP_P,
            "max_tokens": max_tokens or settings.LLM_MAX_TOKENS,
            "stream": False,
        }

        try:
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload,
                )

                if response.status_code != 200:
                    logger.error(f"NVIDIA API Error ({response.status_code}): {response.text}")
                    raise ModelInferenceException(
                        message=f"Lỗi phản hồi từ NVIDIA API (Mã lỗi {response.status_code})",
                        details={"response": response.text},
                    )

                return response.json()
        except httpx.HTTPError as e:
            logger.error(f"NVIDIA API Async request failed: {str(e)}")
            raise ModelInferenceException(
                message=f"Lỗi kết nối bất đồng bộ đến NVIDIA API: {str(e)}"
            )


llm_client = NvidiaLLMClient()
