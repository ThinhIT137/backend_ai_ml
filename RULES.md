# QUY TẮC PHÁT TRIỂN BACKEND AI/ML (RULES.md)

Dự án này là một **Microservice độc lập** phụ trách toàn bộ nghiệp vụ **Trí tuệ nhân tạo (AI) và Học máy (Machine Learning)** cho Hệ thống Tư vấn Tuyển sinh Đại học Giao thông Vận tải (UTC).

Tất cả các thành viên tham gia phát triển và AI Assistant bắt buộc phải tuân thủ nghiêm ngặt các quy tắc sau:

---

### QUY TẮC 1: PHẠM VI HOẠT ĐỘNG (CHỈ LÀM VIỆC TRONG BACKEND AI/ML)
1. **Chỉ làm việc duy nhất trong thư mục `backend_ai_ml/`**: Tuyệt đối không can thiệp, không sửa đổi, không tạo mới hoặc xóa bất kỳ file nào trong thư mục `frontend_admission_UTC/` hay các service khác.
2. **Không quan tâm hay phụ thuộc vào các phần khác**: Nhiệm vụ của ta là hoàn thiện toàn diện, độc lập và chuẩn mực cho microservice AI/ML. Thư mục `frontend_admission_UTC/` nếu có chỉ được xem lướt ở chế độ **ĐỌC (Read-only)** để đối soát cấu trúc dữ liệu, không làm thay việc của frontend.
3. Microservice này giao tiếp độc lập thông qua **RESTful API (JSON)**. Mọi giao tiếp với bên ngoài phải thông qua các endpoints chuẩn tại tầng `router`.

---

### QUY TẮC 2: BẢO TOÀN CẤU TRÚC FILE & THƯ MỤC (PRESERVE STRUCTURE)
1. **Không thay đổi cấu trúc thư mục hiện có**: Tuyệt đối không xóa, không đổi tên, không di chuyển các thư mục đã được định hình (`src/core`, `src/ml`, `src/models`, `src/repositories`, `src/router`, `src/schemas`, `src/services`, `tests`).
2. **Không tự ý thêm file bừa bãi**: Chỉ viết code trực tiếp vào các file Python `.py` trong `src/` và thư mục kiểm thử `tests/`.
3. Các file cấu hình ngoại lệ được phép tồn tại bao gồm:
   - `requirements.txt` (quản lý thư viện)
   - `.env` và `.env.example` (biến môi trường cục bộ)
   - `RULES.md` (file quy tắc này)
   - `TASKS.md` (danh sách công việc)
   - `README.md` (hướng dẫn sử dụng service)
   Ngoài các file trên, không tự ý tạo thêm các file rời rạc ngoài quy hoạch.

---

### QUY TẮC 3: QUẢN LÝ TIẾN ĐỘ THEO TASK (TASK-DRIVEN DEVELOPMENT)
1. **Luôn tham chiếu file `TASKS.md`** trước khi tiến hành viết code hoặc triển khai bất kỳ tính năng nào.
2. **Triển khai tuần tự theo đúng thứ tự ưu tiên**:
   - Hoàn thành theo từng Task trong `TASKS.md`.
   - Sau khi hoàn thành một task, phải cập nhật đánh dấu trạng thái `[x]` vào `TASKS.md`.
3. Không tự ý nhảy cóc, không làm các tính năng chưa có trong danh sách task, không thay đổi phạm vi nghiệp vụ nếu chưa có sự đồng ý của người phụ trách.

---

### QUY TẮC 4: CHUẨN MỰC KIẾN TRÚC PHÂN TẦNG (LAYERED ARCHITECTURE)
Code trong `backend_ai_ml/` phải tuân thủ đúng vai trò của từng tầng:
- **`src/core/`**: Cấu hình hệ thống (`config.py`), xử lý bảo mật (`security.py`), bắt lỗi ngoại lệ (`exceptions.py`).
- **`src/schemas/`**: Định nghĩa cấu trúc DTOs (Data Transfer Objects) bằng Pydantic để validate dữ liệu vào/ra. Không chứa logic nghiệp vụ.
- **`src/ml/`**: Cài đặt thuật toán thuần (Pure Algorithms) & Models:
  - `llm/`: Loader, Prompt templates, RAG pipeline.
  - `mbti/`: Logic chấm điểm trắc nghiệm (Scorer).
  - `prediction/`: Logic dự đoán điểm trúng tuyển và xu hướng điểm chuẩn.
- **`src/services/`**: Tầng điều phối nghiệp vụ (Business Logic). Nhận dữ liệu từ router, gọi tầng ML / Repositories xử lý và trả về kết quả.
- **`src/router/`**: Tầng API Controller. Nhận HTTP Request, validate qua Schema, gọi Service tương ứng và trả HTTP Response. Không viết logic tính toán nặng tại router.
- **`src/models/` & `src/repositories/`**: Quản lý thực thể và truy vấn cơ sở dữ liệu nếu có lưu trữ lịch sử.

---

### QUY TẮC 5: GIAO THỨC PHẢN HỒI API CHUẨN MỰC (API CONTRACT)
1. Mọi API response đều phải trả về định dạng JSON nhất quán:
   - **Thành công (200, 201)**:
     ```json
     {
       "success": true,
       "data": { ... },
       "message": "Thông báo nếu cần"
     }
     ```
   - **Thất bại (400, 404, 500...)**:
     ```json
     {
       "success": false,
       "error": "Mô tả chi tiết lỗi",
       "code": "ERROR_CODE"
     }
     ```
2. Phải bật **CORS Middleware** để hỗ trợ kết nối từ client frontend (mặc định cho phép `http://localhost:3000`).
3. Mọi ngoại lệ (Exceptions) phải được bọc trong bộ xử lý tập trung (`exceptions.py`), tuyệt đối không để crash tiến trình server hoặc rò rỉ stack trace nhạy cảm ra ngoài.

---

### QUY TẮC 6: QUY TẮC ĐẶT TÊN COMMIT (CONVENTIONAL COMMITS)
Khi thực hiện commit mã nguồn lên Git, bắt buộc phải tuân thủ cú pháp chuẩn:
**Cú pháp chuẩn**: `<type>: <mô tả ngắn gọn bằng tiếng Anh>`

Các loại `<type>` quy định:
- **`feat`**: Thêm tính năng mới (Ví dụ: `feat: add login page`, `feat: them tinh nang cham diem mbti`)
- **`fix`**: Sửa lỗi / bug (Ví dụ: `fix: resolve button click crash`, `fix: sua loi load bien moi truong`)
- **`chore`**: Các việc lặt vặt không đổi code chính (Ví dụ: `chore: update .gitignore`, `chore: cap nhat dependencies`)
- **`docs`**: Cập nhật tài liệu, README (Ví dụ: `docs: update installation guide`, `docs: bo sung quy tac commit`)
- **`style`**: Định dạng code, sửa khoảng trắng, chấm phẩy - không ảnh hưởng logic (Ví dụ: `style: reformat imports in app.py`)
- **`refactor`**: Tái cấu trúc code - không đổi tính năng, chỉ tối ưu code (Ví dụ: `refactor: optimize exception handlers`)

● **Yêu cầu về nội dung mô tả (Commit Message Content)**:
- **TUYỆT ĐỐI KHÔNG** đặt tên commit chung chung như: `"hoàn thành task 1"`, `"done task 1"`, `"xong task 2"`.
- **BẮT BUỘC** phải mô tả chính xác công việc cụ thể đã hoàn thành hoặc tính năng vừa được thêm/sửa.
  - *Ví dụ ĐÚNG*:
    - `feat: setup fastapi server core, exception handlers and nvidia llm client`
    - `feat: implement mbti scoring algorithm and major recommendation`
    - `fix: resolve cors parsing and handle unhandled exceptions`
  - *Ví dụ SAI (CẤM DÙNG)*:
    - `feat: hoan thanh task 1`
    - `feat: done task`
    - `fix: xong task 2`

---

### QUY TẮC 7: TIÊU CHUẨN KIỂM THỬ TOÀN DIỆN (COMPREHENSIVE TEST SUITE)
1. **Kiểm thử bao phủ toàn diện (High Coverage)**:
   - Toàn bộ các module của cả Sprint 1 và Sprint 2 bắt buộc phải có test cases đầy đủ trong thư mục `tests/`.
   - Tuyệt đối không viết sơ sài 4-5 test case đối phó; phải bao phủ toàn diện:
     * Unit tests cho các thuật toán pure ML (MBTI scorer, Gale-Shapley simulation, Huber ML regressor, quy đổi phương thức, chuyển đổi chứng chỉ tiếng Anh, điểm ưu tiên BGDĐT, hàm xác suất Sigmoid, phân giỏ nguyện vọng).
     * Integration tests cho toàn bộ tầng Repositories, Services, Models.
     * API integration tests qua FastAPI `TestClient` cho toàn bộ 21 endpoints.
     * Boundary & Edge case tests: Điểm chạm sàn (0), điểm tối đa (30), điểm sát mốc 22.5, tổ hợp thiếu môn, chứng chỉ ngoài thang, mã ngành không tồn tại (404), kịch bản mô phỏng vĩ mô.
2. **Quy chuẩn mã nguồn Test**:
   - Tuân thủ nghiêm ngặt quy tắc: **0 comment (`#`) và 0 docstring (`"""..."""`)** trong toàn bộ các file Python của `tests/`.
   - Đặt tên hàm test rõ nghĩa theo chuẩn ngữ nghĩa tiếng Anh (ví dụ: `test_calculate_priority_with_linear_discount_above_22_5()`).
   - 100% test cases trong test suite phải chạy thành công (Pass) khi thực thi `pytest`.


