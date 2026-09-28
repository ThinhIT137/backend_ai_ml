import logging
import uuid
from typing import Any, Dict, List, Optional

from src.core.exceptions import AppException, NotFoundException
from src.ml.llm.loader import llm_client
from src.ml.llm.prompt_templates import (
    SYSTEM_PROMPT_UTC_ADVISOR,
    build_rag_prompt,
    get_default_suggested_questions,
)
from src.ml.llm.rag import rag_pipeline
from src.repositories.chat_repository import chat_repository
from src.schemas.chat_schema import (
    ChatRequest,
    ChatResponseData,
    ChatSourceItem,
    KnowledgeCreateRequest,
    KnowledgeItemSchema,
    KnowledgeSyncResponse,
    KnowledgeUpdateRequest,
)

logger = logging.getLogger(__name__)


class ChatService:
    def sync_knowledge(self) -> KnowledgeSyncResponse:
        db_items = chat_repository.get_active_tri_thuc()
        total = rag_pipeline.reload(db_items=db_items)

        logger.info(f"Đã đồng bộ RAG: tổng cộng {total} mục tri thức từ Supabase.")
        return KnowledgeSyncResponse(
            success=True,
            total_documents=total,
            supabase_faq_count=total,
            chunks_count=0,
            message=f"Đồng bộ thành công {total} mục tri thức từ CSDL Supabase vào hệ thống RAG.",
        )

    def ask(self, request: ChatRequest) -> ChatResponseData:
        active_session = request.session_id or f"chat_{uuid.uuid4().hex[:12]}"
        query = request.question or request.message or ""

        retrieved_chunks = rag_pipeline.retrieve(query=query, top_k=3)

        user_prompt = build_rag_prompt(query=query, context_chunks=retrieved_chunks)

        messages = [
            {"role": "system", "content": SYSTEM_PROMPT_UTC_ADVISOR},
            {"role": "user", "content": user_prompt},
        ]

        answer = ""
        try:
            resp = llm_client.generate(
                messages=messages,
                max_tokens=1024,
                temperature=0.3,
                top_p=0.9,
            )
            choices = resp.get("choices", [])
            if choices:
                answer = choices[0].get("message", {}).get("content", "").strip()
        except Exception as e:
            logger.error(f"Lỗi gọi LLM Client trong ChatService: {str(e)}")
            answer = (
                "Chào bạn, hệ thống AI đang trong quá trình bảo trì kết nối dịch vụ tính toán. "
                "Tuy nhiên, căn cứ theo thông tin đào tạo của Trường ĐH Giao thông Vận tải, "
                "bạn vui lòng liên hệ trực tiếp Hotline Tuyển sinh UTC: (024) 3766 3311 để được hỗ trợ tốt nhất."
            )

        if not answer:
            answer = (
                "Rất tiếc hiện tại mình chưa có đủ thông tin chi tiết về câu hỏi này trong cơ sở dữ liệu. "
                "Bạn vui lòng tham khảo trang tuyển sinh chính thức tuyensinh.utc.edu.vn hoặc Hotline (024) 3766 3311 nhé."
            )

        sources: List[ChatSourceItem] = []
        for c in retrieved_chunks:
            content_snippet = c.get("content", "")
            if len(content_snippet) > 200:
                content_snippet = content_snippet[:200] + "..."

            sources.append(
                ChatSourceItem(
                    doc_label=c.get("doc_label", "Tài liệu đào tạo UTC"),
                    breadcrumb=c.get("breadcrumb"),
                    page_range=str(c.get("page_range", "")),
                    content_snippet=content_snippet,
                    score=c.get("score"),
                )
            )

        suggested = get_default_suggested_questions(query)

        return ChatResponseData(
            answer=answer,
            session_id=active_session,
            sources=sources,
            suggested_questions=suggested,
        )

    def get_knowledge_list(self) -> List[KnowledgeItemSchema]:
        rows = chat_repository.get_all_tri_thuc()
        return [KnowledgeItemSchema(**r) for r in rows]

    def create_knowledge(self, req: KnowledgeCreateRequest) -> KnowledgeItemSchema:
        item = chat_repository.create_tri_thuc(
            chu_de=req.chu_de or "",
            cau_hoi_mau=req.cau_hoi_mau,
            noi_dung=req.noi_dung or "",
            admin_id=req.ma_admin_phu_trach,
        )
        if not item:
            raise AppException("Không thể thêm mới mục tri thức vào CSDL")
        self.sync_knowledge()
        return KnowledgeItemSchema(**item)

    def update_knowledge(self, ma_tri_thuc: str, req: KnowledgeUpdateRequest) -> KnowledgeItemSchema:
        item = chat_repository.update_tri_thuc(
            ma_tri_thuc=ma_tri_thuc,
            chu_de=req.chu_de,
            cau_hoi_mau=req.cau_hoi_mau,
            noi_dung=req.noi_dung,
            trang_thai=req.trang_thai,
        )
        if not item:
            raise NotFoundException(f"Không tìm thấy bản ghi tri thức {ma_tri_thuc}")
        self.sync_knowledge()
        return KnowledgeItemSchema(**item)

    def delete_knowledge(self, ma_tri_thuc: str) -> bool:
        ok = chat_repository.delete_tri_thuc(ma_tri_thuc)
        if not ok:
            raise NotFoundException(f"Không tìm thấy hoặc không thể xóa bản ghi {ma_tri_thuc}")
        self.sync_knowledge()
        return True


chat_service = ChatService()