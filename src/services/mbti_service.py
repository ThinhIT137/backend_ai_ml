import logging
from typing import Any, Dict, List, Optional
from src.core.exceptions import NotFoundException, ValidationException
from src.ml.mbti.scorer import calculate_mbti_result
from src.repositories.mbti_repository import mbti_repository
from src.schemas.mbti_schema import (
    MBTIHistoryItem,
    MBTIQuestion,
    MBTIResultData,
    MBTISubmitRequest,
)

logger = logging.getLogger(__name__)


class MBTIService:
    def get_questions(self) -> List[MBTIQuestion]:
        raw_questions = mbti_repository.get_questions()
        return [
            MBTIQuestion(
                id=q["id"],
                text=q["text"],
                dimension=q["dimension"],
                category=q["dimension"],
                positive_trait=q["positive_trait"],
                context_field=q.get("context_field"),
            )
            for q in raw_questions
        ]

    def process_submission(self, request: MBTISubmitRequest) -> MBTIResultData:
        if not request.answers:
            raise ValidationException("Danh sách câu trả lời không được để trống")

        q_map = mbti_repository.get_question_map()
        valid_question_ids = set(q_map.keys())
        answered_ids = set()

        for ans in request.answers:
            if ans.question_id not in valid_question_ids:
                raise ValidationException(
                    f"Câu hỏi ID {ans.question_id} không hợp lệ trong bộ đề thi UTC"
                )
            if ans.question_id in answered_ids:
                raise ValidationException(
                    f"Câu hỏi ID {ans.question_id} bị trả lời trùng lặp"
                )
            answered_ids.add(ans.question_id)

        result = calculate_mbti_result(
            answers=request.answers,
            student_name=request.student_name,
            session_id=request.session_id,
            cccd=request.cccd,
            include_ai_advice=request.include_ai_advice,
        )

        full_report_data = result.model_dump(mode="json")
        saved_id = mbti_repository.save_result(
            session_id=result.session_id or "anonymous_session",
            nhom_tinh_cach=result.mbti_type,
            goi_y_nganh=full_report_data,
            cccd=result.cccd,
        )
        result.result_id = saved_id

        logger.info(
            f"Đã xử lý bài thi MBTI cho thí sinh '{request.student_name or 'Ẩn danh'}': Kết quả {result.mbti_type} ({result.type_name}), mã kết quả: {saved_id}"
        )
        return result

    def get_result(self, result_id: str) -> MBTIResultData:
        data = mbti_repository.get_result_by_id(result_id)
        if not data:
            raise NotFoundException(f"Không tìm thấy kết quả trắc nghiệm với mã: {result_id}")
        return MBTIResultData.model_validate(data)

    def get_history(
        self, session_id: Optional[str] = None, cccd: Optional[str] = None
    ) -> List[MBTIHistoryItem]:
        if not session_id and not cccd:
            raise ValidationException("Cần cung cấp ít nhất session_id hoặc cccd để tra cứu lịch sử")
        items = mbti_repository.get_history(session_id=session_id, cccd=cccd)
        return [MBTIHistoryItem.model_validate(i) for i in items]


mbti_service = MBTIService()