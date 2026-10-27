import re
from typing import Any, Dict, List, Optional

SYSTEM_PROMPT_UTC_ADVISOR = (
    "Bạn là Trợ lý AI Cố vấn Tuyển sinh và Đào tạo chính thức của Trường Đại học Giao thông Vận tải (UTC).\n"
    "Nhiệm vụ duy nhất của bạn là giải đáp chính xác, thân thiện, dễ hiểu các thắc mắc của thí sinh và phụ huynh "
    "về tuyển sinh, ngành đào tạo, chương trình học, điểm chuẩn, quy chế tín chỉ, học phí, học bổng và đời sống sinh viên tại Trường Đại học Giao thông Vận tải (UTC).\n\n"
    "CÁC NGUYÊN TẮC BẮT BUỘC:\n"
    "1. GIỚI HẠN PHẠM VI (QUAN TRỌNG NHẤT):\n"
    "   - Bạn CHỈ trả lời các câu hỏi liên quan đến Trường Đại học Giao thông Vận tải (UTC), ngành học, tuyển sinh và đào tạo tại UTC.\n"
    "   - TUYỆT ĐỐI KHÔNG giải bài tập (toán, lý, hóa, văn, lập trình,...), không trả lời câu hỏi kiến thức chung, đố vui, giải trí hay các chủ đề ngoài tuyển sinh UTC.\n"
    "   - TUYỆT ĐỐI KHÔNG tư vấn, giới thiệu, so sánh hay gợi ý ngành học của các trường đại học khác (ví dụ: Bách Khoa, Kinh Tế Quốc Dân, Ngoại Thương,...). Chỉ tập trung vào các ngành đào tạo và thế mạnh của UTC.\n"
    "   - Nếu câu hỏi KHÔNG LIÊN QUAN đến tuyển sinh hoặc ngành học của Trường Đại học Giao thông Vận tải (UTC), bạn PHẢI TỪ CHỐI lịch sự theo mẫu:\n"
    "     'Tôi là trợ lý AI tư vấn tuyển sinh của Trường Đại học Giao thông Vận tải (UTC). Tôi không thể trả lời các câu hỏi không liên quan tới ngành học hoặc thông tin tuyển sinh của trường. Nếu bạn quan tâm đến các ngành đào tạo, phương thức xét tuyển hoặc điểm chuẩn tại UTC, tôi rất sẵn lòng hỗ trợ bạn!'\n"
    "2. Căn cứ thông tin: Ưu tiên trả lời dựa trên CĂN CỨ TÀI LIỆU THAM CHIẾU được cung cấp bên dưới.\n"
    "3. Trích dẫn nguồn: Khi trả lời các quy chế hoặc thông số cụ thể, hãy trích dẫn ngắn gọn nguồn "
    "(ví dụ: 'Theo Sổ tay Sinh viên K67', 'Theo Niên giám K64', 'Theo dữ liệu tuyển sinh UTC').\n"
    "4. Định dạng: Trình bày mạch lạc, sử dụng gạch đầu dòng và in đậm các từ khóa quan trọng.\n"
    "5. Tính trung thực: Tuyệt đối không bịa đặt thông tin khi không có trong tài liệu. Nếu câu hỏi trong phạm vi tuyển sinh UTC nhưng vượt quá dữ liệu hiện có, "
    "hãy khiêm tốn thông báo và hướng dẫn thí sinh liên hệ Hotline Tuyển sinh UTC: (024) 3766 3311 hoặc Website: tuyensinh.utc.edu.vn."
)

OUT_OF_SCOPE_REFUSAL = (
    "Tôi là trợ lý AI tư vấn tuyển sinh của Trường Đại học Giao thông Vận tải (UTC). "
    "Tôi không thể trả lời các câu hỏi không liên quan tới ngành học hoặc thông tin tuyển sinh của trường. "
    "Nếu bạn có thắc mắc về các ngành đào tạo, phương thức xét tuyển, điểm chuẩn, học phí hoặc đời sống sinh viên tại UTC, "
    "tôi rất sẵn lòng hỗ trợ bạn!"
)

OUT_OF_SCOPE_PATTERNS = [
    r"\b(?:phương\s+trình|hệ\s+phương\s+trình|bất\s+phương\s+trình|tích\s+phân|đạo\s+hàm|nguyên\s+hàm|ma\s+trận)\b",
    r"\b(?:giải\s+toán|bài\s+toán|giải\s+bài|làm\s+bài\s+tập|giải\s+hộ|giải\s+giúp)\b",
    r"\b(?:viết\s+code|viết\s+chương\s+trình|code\s+python|code\s+java|code\s+c\+\+|lập\s+trình\s+giúp)\b",
    r"\b(?:làm\s+thơ|soạn\s+văn|phân\s+tích\s+bài\s+thơ|kể\s+chuyện\s+cười)\b",
    r"\b(?:thời\s+tiết\s+hôm\s+nay|giá\s+vàng|tỷ\s+giá|chứng\s+khoán|kết\s+quả\s+xổ\s+số)\b",
]

OTHER_UNIVERSITIES_PATTERNS = [
    r"\b(?:bách\s+khoa|hust|kinh\s+tế\s+quốc\s+dân|neu|ngoại\s+thương|ftu|học\s+viện\s+ngân\s+hàng|học\s+viện\s+tài\s+chính|bưu\s+chính\s+viễn\s+thông|ptit|đại\s+học\s+fpt|rmit)\b",
]

UTC_KEYWORDS = [
    "utc", "giao thông", "gtvt", "trường mình", "trường ta"
]


def is_out_of_scope_query(query: str) -> bool:
    q = query.lower().strip()
    if not q:
        return False
    for pat in OUT_OF_SCOPE_PATTERNS:
        if re.search(pat, q, re.IGNORECASE):
            return True
    has_other_uni = any(re.search(pat, q, re.IGNORECASE) for pat in OTHER_UNIVERSITIES_PATTERNS)
    has_utc = any(k in q for k in UTC_KEYWORDS)
    if has_other_uni and not has_utc:
        return True
    return False


def build_rag_prompt(query: str, context_chunks: List[Dict[str, Any]]) -> str:
    if not context_chunks:
        return f"CÂU HỎI CỦA THÍ SINH / PHỤ HUYNH:\n{query}"

    context_parts = []
    for idx, c in enumerate(context_chunks, 1):
        doc_label = c.get("doc_label", "Tài liệu đào tạo UTC")
        breadcrumb = c.get("breadcrumb", "")
        page_range = c.get("page_range", "")
        content = c.get("content", "").strip()

        header = f"--- [TÀI LIỆU THAM CHIẾU {idx}: {doc_label}] ---"
        location = f"Vị trí: {breadcrumb}" if breadcrumb else ""
        pages = f"Trang: {page_range}" if page_range else ""
        meta = " | ".join(filter(None, [location, pages]))

        block = f"{header}\n{meta}\nNội dung:\n{content}\n" if meta else f"{header}\nNội dung:\n{content}\n"
        context_parts.append(block)

    full_context = "\n".join(context_parts)
    return (
        f"CĂN CỨ THÔNG TIN ĐÀO TẠO & TUYỂN SINH UTC:\n"
        f"{full_context}\n"
        f"==================================================\n"
        f"CÂU HỎI CỦA THÍ SINH / PHỤ HUYNH:\n{query}\n\n"
        f"HÃY TRẢ LỜI CÂU HỎI TRÊN DỰA VÀO CÁC CĂN CỨ ĐÃ ĐƯỢC CUNG CẤP (LƯU Ý: TỪ CHỐI NẾU CÂU HỎI NGOÀI PHẠM VI UTC):"
    )


def get_default_suggested_questions(query: str = "") -> List[str]:
    q_lower = query.lower()
    if any(k in q_lower for k in ["điểm", "chuẩn", "xét tuyển", "đỗ", "trúng tuyển"]):
        return [
            "Điểm chuẩn ngành Logistics và Quản lý chuỗi cung ứng 2025?",
            "Phương thức xét tuyển bằng học bạ gồm những điều kiện gì?",
            "Bằng IELTS 6.5 được quy đổi thành bao nhiêu điểm?",
        ]
    elif any(k in q_lower for k in ["học phí", "học bổng", "miễn giảm", "chi phí", "tiền học"]):
        return [
            "Các mức học bổng khuyến khích học tập tại UTC như thế nào?",
            "Đối tượng nào được miễn giảm 100% học phí tại UTC?",
            "Quy trình xin cấp giấy xác nhận vay vốn tín dụng sinh viên?",
        ]
    elif any(k in q_lower for k in ["ngành", "cntt", "công nghệ", "kỹ thuật", "môn", "tín chỉ"]):
        return [
            "Ngành Công nghệ thông tin học những môn gì ở các kỳ đầu?",
            "Mô hình tích hợp Cử nhân - Kỹ sư tại UTC là gì?",
            "Chuẩn đầu ra tiếng Anh khi tốt nghiệp UTC là bao nhiêu?",
        ]
    return [
        "Điểm chuẩn ngành Công nghệ thông tin UTC năm 2025?",
        "Thời gian nộp hồ sơ xét tuyển sớm K66 là khi nào?",
        "Chính sách học bổng dành cho tân sinh viên xuất sắc?",
        "Ký túc xá Đại học GTVT có đủ chỗ cho sinh viên năm nhất không?",
    ]
