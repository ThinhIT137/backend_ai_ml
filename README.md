This is a [FastAPI](https://fastapi.tiangolo.com) microservice providing AI/ML services for the UTC Admission Portal (MBTI Career Assessment, RAG Chatbot Consultation, and Admission Predictions).

## Getting Started

### 1. Tạo môi trường ảo (Virtual Environment)

```bash
# Tạo virtual environment
python -m venv venv

# Kích hoạt trên Windows:
venv\Scripts\activate

# Kích hoạt trên Linux/macOS:
source venv/bin/activate
```

### 2. Cài đặt các thư viện phụ thuộc

```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường

Sao chép file mẫu `.env.example` thành `.env` và điền các khóa cấu hình:

```bash
cp .env.example .env
```

Các biến môi trường cơ bản:
- `NVIDIA_API_KEY`: API Key kết nối mô hình LLaMA qua NVIDIA NIM.
- `DATABASE_URL`: Connection string PostgreSQL kết nối tới Supabase.
- `CORS_ORIGINS`: Danh sách domain Frontend được phép kết nối (mặc định `http://localhost:3000`).

### 4. Chạy server phát triển (Development Server)

```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
# hoặc
python app.py
```

Server sẽ khởi chạy tại: [http://localhost:8000](http://localhost:8000)

---

## Tài liệu API tương tác (Interactive API Docs)

FastAPI tự động sinh tài liệu chuẩn OpenAPI (Swagger UI) tại:

- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## Các nhóm API chính

### 1. Trắc nghiệm tính cách MBTI & Định hướng ngành UTC
- `GET /api/mbti/questions`: Lấy 20 câu hỏi trắc nghiệm chuẩn từ CSDL `cau_hoi_mbti`.
- `POST /api/mbti/submit`: Nộp bài, tính toán 4 trục tính cách, đề xuất top ngành học UTC và lưu kết quả vào `ket_qua_trac_nghiem`.
- `GET /api/mbti/result/{result_id}`: Xem chi tiết báo cáo phân tích tính cách chuyên sâu theo mã kết quả.
- `GET /api/mbti/history`: Tra cứu lịch sử các bài trắc nghiệm đã làm theo số CCCD hoặc `session_id`.

### 2. Dự đoán điểm chuẩn & Mô phỏng kịch bản (Sprint 2)
- `GET /api/predict/all-benchmarks`: Lấy điểm chuẩn dự đoán 2026 của toàn bộ 54 chương trình đào tạo UTC Hà Nội kèm quy đổi 4 phương thức (`PT1`, `PT2`, `PT3`, `PT4`).
- `GET /api/predict/benchmark/{ma_chuong_trinh}`: Xem chi tiết điểm chuẩn dự đoán 2026 cho 1 mã chương trình đào tạo cụ thể.
- `POST /api/predict/simulate-scenario`: Mô phỏng giả lập điểm chuẩn khi chỉ tiêu tuyển sinh thay đổi hoặc phổ điểm thi vĩ mô biến động.

### 3. Đánh giá xác suất trúng tuyển & Chiến lược nguyện vọng (Sprint 2)
- `POST /api/predict/admission-chance`: Tính điểm xét tuyển cá nhân (tự động đổi điểm IELTS/TOEFL/TOEIC, tính điểm ưu tiên BGDĐT giảm trừ $\ge 22.5$, chọn tổ hợp tối ưu), độ lệch điểm, xác suất đỗ (0-100%) và lời khuyên chuyên gia.
- `POST /api/predict/recommend-majors`: Quét toàn bộ 54 ngành UTC Hà Nội và xếp vào 3 giỏ nguyện vọng ("Kim tự tháp an toàn"): An toàn ($\ge 85\%$), Vừa sức ($65\%-85\%$), Thử thách ($45\%-65\%$) kèm chiến lược xếp NV1 $\rightarrow$ NV5+.

### 4. Trợ lý AI Chatbot & Quản lý tri thức RAG
- `POST /api/chat`: Hỏi đáp tư vấn tuyển sinh thông minh với trợ lý AI (truy xuất từ 132 mục tri thức tuyển sinh UTC).
- `GET /api/chat/knowledge`: Lấy danh sách dữ liệu tri thức đào tạo từ Supabase.
- `POST /api/chat/knowledge`: Thêm mới mục tri thức vào CSDL và tự động cập nhật bộ nhớ RAG.
- `PUT /api/chat/knowledge/{ma_tri_thuc}`: Cập nhật mục tri thức.
- `DELETE /api/chat/knowledge/{ma_tri_thuc}`: Xóa mục tri thức.
- `POST /api/chat/sync-knowledge`: Đồng bộ lại toàn bộ dữ liệu CSDL vào chỉ mục tìm kiếm RAG trên RAM.

---

## Hướng dẫn kết nối từ Frontend Next.js

1. Khai báo biến môi trường trong file `.env` của Frontend:
   ```env
   NEXT_PUBLIC_AI_API_URL="http://localhost:8000"
   ```
2. Gọi các API Backend thông qua fetch / axios tương ứng:
   - Trang `/tinh-diem-quy-doi`: Gọi `POST /api/predict/admission-chance` và `POST /api/predict/recommend-majors`.
   - Trang `/trac-nghiem-mbti`: Gọi `GET /api/mbti/questions` và `POST /api/mbti/submit`.
   - Trang `/hoi-dap-ai`: Gọi `POST /api/chat`.
   - Trang `/admin/du-lieu-chatbot-ai`: Gọi `POST /api/chat/sync-knowledge` sau mỗi thao tác cập nhật tri thức.
