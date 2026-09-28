import logging
from typing import List

from src.core.exceptions import ValidationException
from src.ml.mbti.scorer import MBTI_QUESTIONS, calculate_mbti_result
from src.schemas.mbti_schema import (
    MBTIQuestion,
    MBTIResultData,
    MBTISubmitRequest,
)

logger = logging.getLogger(__name__)


class MBTIService:
    def get_questions(self) -> List[MBTIQuestion]:
        return [
            MBTIQuestion(
                id=q["id"],
                text=q["text"],
                dimension=q["dimension"],
                category=q["dimension"],
                positive_trait=q["positive_trait"],
                context_field=q.get("context_field"),
            )
            for q in MBTI_QUESTIONS
        ]

    def process_submission(self, request: MBTISubmitRequest) -> MBTIResultData:
        if not request.answers:
            raise ValidationException("Danh sách câu trả lời không được để trống")

        valid_question_ids = {q["id"] for q in MBTI_QUESTIONS}
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

        logger.info(
            f"Đã xử lý bài thi MBTI cho thí sinh '{request.student_name or 'Ẩn danh'}': Kết quả {result.mbti_type} ({result.type_name})"
        )
        return result


mbti_service = MBTIService()