# BÁO CÁO ĐỐI SOÁT TÍCH HỢP FRONTEND - BACKEND AI/ML
## Sprint: Trắc nghiệm MBTI, Quản lý dữ liệu Chatbot & Hỏi đáp AI Chatbot

> **Dự án**: Tuyển sinh Đại học Giao thông Vận tải (UTC)
> **Thời gian thực hiện**: 2026-09-28
> **Microservice Backend**: `backend_ai_ml` (FastAPI, Python 3.10)
> **Frontend**: `frontend_admission_UTC` (Next.js 15, React 19, TypeScript)
> **Cơ sở dữ liệu**: Supabase PostgreSQL

---

## 📌 1. BẢNG TỔNG QUAN ĐỐI SOÁT

| TT | Nhiệm vụ Sprint | Đường dẫn Frontend | Trạng thái đối soát | Đánh giá mức độ đáp ứng |
| :-: | :--- | :--- | :-: | :--- |
| **1** | **Trắc nghiệm MBTI** | `/trac-nghiem-mbti` | **100% Khớp** | Tương thích hoàn toàn interface câu hỏi và payload kết quả phân tích |
| **2** | **Quản lý dữ liệu huấn luyện Chatbot** | `/admin/du-lieu-chatbot-ai` | **100% Khớp** | Đầy đủ trọn bộ CRUD, hỗ trợ tên trường song ngữ, tự động re-index RAG |
| **3** | **Hỏi đáp AI Chatbot** | `/hoi-dap-ai` | **100% Khớp** | Trả lời tiếng Việt từ RAG CSDL 131 chunks, kèm nguồn trích dẫn & câu hỏi gợi ý |

---

## 📋 2. CHI TIẾT ĐỐI SOÁT VÀ NÂNG CẤP HỆ THỐNG

### 🎯 2.1. Nhiệm vụ 1: Trắc nghiệm MBTI (`/trac-nghiem-mbti`)

#### Cấu trúc Frontend:
- **State câu hỏi**: Quản lý dạng `mockQuestions: Question[]`:
  - `id: number`
  - `text: string`
  - `category: "EI" | "SN" | "TF" | "JP"`
- **State làm bài**: `answers: Record<number, number>` (thang điểm 1-5).
- **Trường thông tin phụ**: `studentName: string`.
- **Giao diện kết quả**: Huy hiệu nhóm tính cách, tên danh xưng, đoạn văn tóm tắt tính cách, môi trường học tập lý tưởng và danh sách top ngành học UTC kèm link chuyển hướng `/tra-cuu-nganh-hoc/${major.slug}`.

#### Khớp nối Backend AI/ML:
- `GET /api/mbti/questions`: Trả về 20 câu hỏi định hướng nghề nghiệp kỹ sư/kinh tế UTC kèm trường `category: "EI" | "SN" | "TF" | "JP"` khớp 1:1 với Frontend.
- `POST /api/mbti/submit`:
  - Chấp nhận `studentName` (camelCase) và `student_name` (snake_case).
  - Chấp nhận `answers` cả dạng Dict `{1: 5, 2: 4}` lẫn List `[{"question_id": 1, "score": 5}]`.
  - Kết quả trả về chứa: `mbti_type`, `type_name`, `personality_summary`, `suitable_environment`, `dimension_scores` (4 trục %), `recommended_majors` (với `major_code`, `major_name` truy vấn động từ CSDL Supabase và `slug` tĩnh điều hướng router).

---

### 📚 2.2. Nhiệm vụ 2: Quản lý dữ liệu huấn luyện Chatbot (`/admin/du-lieu-chatbot-ai`)

#### Cấu trúc Frontend:
- **Giao diện**:
  - Bảng danh sách `DataTable` hiển thị: Chủ đề dữ liệu (`topic`), Câu hỏi mẫu (`question`), Phản hồi chuẩn AI (`answer`), Trạng thái (`status`).
  - Modal Form: "Thêm Dữ Liệu KB Mới" và "Sửa Dữ Liệu AI".
  - Dialog: "Xác Nhận Xóa Dữ Liệu AI".
- **API Route Next.js**: `app/api/du-lieu-chatbot-ai/route.ts` tương tác trực tiếp với bảng `tri_thuc_ai` trên Supabase.

#### Nâng cấp Backend AI/ML:
- **Hỗ trợ trường song ngữ (Dual Fields)** trong `KnowledgeItemSchema`:
  - Trả về đồng thời cả:
    - Tên chuẩn CSDL: `ma_tri_thuc`, `chu_de`, `cau_hoi_mau`, `noi_dung`, `trang_thai`.
    - Tên chuẩn Frontend: `id`, `topic`, `question`, `answer`, `status`.
- **Trọn bộ API RESTful CRUD**:
  - `GET /api/chat/knowledge`: Lấy toàn bộ danh sách tri thức từ Supabase.
  - `POST /api/chat/knowledge`: Thêm tri thức mới vào CSDL và tự động reload chỉ mục BM25 RAG.
  - `PUT /api/chat/knowledge/{ma_tri_thuc}`: Cập nhật tri thức và tự động reload chỉ mục RAG.
  - `DELETE /api/chat/knowledge/{ma_tri_thuc}`: Xóa tri thức và tự động reload chỉ mục RAG.
  - `POST /api/chat/sync-knowledge`: Đồng bộ tức thời dữ liệu khi có thay đổi ngoài hệ thống.

---

### 💬 2.3. Nhiệm vụ 3: Hỏi đáp AI Chatbot (`/hoi-dap-ai`)

#### Cấu trúc Frontend:
- Hộp chat trao đổi với trợ lý AI: danh sách tin nhắn `{ id, sender: "user" | "bot", text, time }`.
- Thanh gợi ý câu hỏi mẫu nhanh (Prompts bar).
- Ô nhập liệu và nút Gửi câu hỏi.

#### Khớp nối Backend AI/ML:
- `POST /api/chat`:
  - Chấp nhận cả trường `question` lẫn `message`.
  - Cơ chế RAG BM25 tiếng Việt (unigrams + bigrams) truy xuất top 3 đoạn ngữ cảnh liên quan nhất từ 131 chunks dữ liệu thực tế trong CSDL Supabase.
  - Gọi mô hình LLM `meta/llama-3.2-11b-vision-instruct` tổng hợp câu trả lời theo đúng phong cách chuyên gia tư vấn tuyển sinh UTC.
  - Trả về `sources` (minh bạch tài liệu nguồn) và `suggested_questions` (gợi ý các câu hỏi liên quan tiếp theo).
  - Tích hợp fallback an toàn: không bao giờ để xảy ra lỗi 500 khi mạng ngoài tới NVIDIA API bị timeout.

---

## 🧪 3. KẾT QUẢ KIỂM THỬ TỰ ĐỘNG TOÀN DIỆN

Hệ thống đã chạy kiểm thử tự động toàn diện qua `FastAPI TestClient`:
- `GET /api/mbti/questions`: **200 OK** (20 câu hỏi).
- `POST /api/mbti/submit`: **200 OK** (Xử lý chính xác định dạng React state `{1: 5, 2: 1, ...}`).
- `GET /api/chat/knowledge`: **200 OK** (Dual fields `topic`/`chu_de`, `id`/`ma_tri_thuc`, `answer`/`noi_dung`).
- `POST /api/chat/knowledge`: **201 Created** (Thêm mới và tự động cập nhật RAG RAM).
- `PUT /api/chat/knowledge/{id}`: **200 OK** (Cập nhật và tự động cập nhật RAG RAM).
- `DELETE /api/chat/knowledge/{id}`: **200 OK** (Xóa và tự động cập nhật RAG RAM).
- `POST /api/chat`: **200 OK** (Truy xuất đúng ngữ cảnh, phản hồi tiếng Việt chuẩn mực).
- **Quy chuẩn mã nguồn**: 100% tuân thủ **0 comments (`#`)** và **0 docstrings (`"""..."""`)**.
