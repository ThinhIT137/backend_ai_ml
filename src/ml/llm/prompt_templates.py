from typing import Any, Dict, List, Optional

SYSTEM_PROMPT_UTC_ADVISOR = (
    "Bạn là Trợ lý AI Cố vấn Tuyển sinh và Đào tạo chính thức của Trường Đại học Giao thông Vận tải (UTC).\n"
    "Nhiệm vụ của bạn là giải đáp chính xác, thân thiện, dễ hiểu mọi thắc mắc của thí sinh và phụ huynh "
    "về tuyển sinh, ngành đào tạo, điểm chuẩn, quy chế tín chỉ, học bổng và đời sống sinh viên UTC.\n\n"
    "CÁC NGUYÊN TẮC BẮT BUỘC:\n"
    "1. Căn cứ thông tin: Ưu tiên trả lời dựa trên CĂN CỨ TÀI LIỆU THAM CHIẾU được cung cấp bên dưới.\n"
    "2. Trích dẫn nguồn: Khi trả lời các quy chế hoặc thông số cụ thể, hãy trích dẫn ngắn gọn nguồn "
    "(ví dụ: 'Theo Sổ tay Sinh viên K67', 'Theo Niên giám K64', 'Theo dữ liệu tuyển sinh UTC').\n"
    "3. Định dạng: Trình bày mạch lạc, sử dụng gạch đầu dòng và in đậm các từ khóa quan trọng.\n"
    "4. Tính trung thực: Tuyệt đối không bịa đặt thông tin khi không có trong tài liệu. Nếu câu hỏi vượt quá dữ liệu, "
    "hãy khiêm tốn thông báo và hướng dẫn thí sinh liên hệ Hotline Tuyển sinh UTC: (024) 3766 3311 hoặc Website: tuyensinh.utc.edu.vn."
)


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
        f"HÃY TRẢ LỜI CÂU HỎI TRÊN DỰA VÀO CÁC CĂN CỨ ĐÃ ĐƯỢC CUNG CẤP:"
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
