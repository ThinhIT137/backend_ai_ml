# KẾ HOẠCH & DANH SÁCH TASK TRIỂN KHAI BACKEND AI/ML (TASKS.md)

Tài liệu này định nghĩa chi tiết toàn bộ các đầu việc cần thực hiện cho **Microservice Backend AI/ML Tuyển sinh UTC**, được tổ chức phân bổ theo từng Sprint phát triển.
Mọi lập trình viên và AI Assistant cần tuân thủ nghiêm ngặt các quy định trong `RULES.md` khi triển khai.

---

## 📌 BẢNG TIẾN ĐỘ TỔNG QUAN THEO SPRINT

### SPRINT 1: NỀN TẢNG CORE, TRẮC NGHIỆM MBTI & HỎI ĐÁP AI CHATBOT (Hoàn thành 100%)
- [x] **Giai đoạn 1: Nền tảng Core & Môi trường Microservice**
- [x] **Giai đoạn 2: Module MBTI (Trắc nghiệm tính cách & Định hướng ngành UTC)**
- [x] **Giai đoạn 3: Module LLM & RAG (Trợ lý Chatbot tư vấn & Quản lý tri thức huấn luyện)** *(Trước là Giai đoạn 4)*

### SPRINT 2: TƯ VẤN HƯỚNG NGHIỆP, DỰ ĐOÁN ĐIỂM CHUẨN & XÁC SUẤT TRÚNG TUYỂN (Hoàn thành 100%)
- [x] **Task 1: Xem kết quả tư vấn hướng nghiệp (Lưu trữ CSDL, Báo cáo chuyên sâu & Lịch sử)** *(Hoàn thành 100%)*
- [x] **Task 2: Dự đoán điểm chuẩn ngành học** *(Hoàn thành 100%: Mô hình điểm chuẩn động realtime & tích hợp tin tức thị trường)*
- [x] **Task 3: Dự đoán khả năng trúng tuyển** *(Hoàn thành 100%: Xác suất trúng tuyển theo phân phối động & chiến lược kim tự tháp)*
- [x] **Task 4: Tầng lưu trữ** *(Hoàn thành 100%: In-memory DTO, tracking & CSDL chuẩn Supabase)*
- [x] **Task 5: Hoàn thiện Endpoints Router & Kiểm thử tích hợp** *(Hoàn thành 100%: 215/215 tests pass 100%)*

### SPRINT 3: DỰ BÁO ĐIỂM ĐỘNG REAL-TIME, COLD-START 2027 & MODULE TIN TỨC THỊ TRƯỜNG (Hoàn thành 100%)
- [x] **Task 1: Cơ chế Cập nhật Điểm chuẩn Động liên tục từ lúc mở cổng (Real-time Dynamic Cutoff Updating & Bayesian Influx)**
- [x] **Task 2: Module Phân tích Tin tức & Xu hướng Xã hội tác động Điểm chuẩn (News Sentiment & Market Trend Engine)**
- [x] **Task 3: Mô hình Ngoại suy Đường cong Nộp hồ sơ (S-Curve Influx) & Bộ Lọc Ảo Đa Phương Thức (Virtual Filtering)**
- [x] **Task 4: Thuật toán Cold-Start cho Môn thi mới năm 2027 (Quy đổi phân vị tương đương toàn quốc - Percentile Equating)**
- [x] **Task 5: Thuật toán Cold-Start cho Ngành học mới mở năm 2027 (Học chuyển giao cụm ngành tương đồng - Transfer Learning & KNN)**
- [x] **Task 6: Đo lường Tín hiệu Hành vi Sớm (Early Telemetry) & Ước lượng Độ bất định (Dynamic Confidence Interval)**
- [x] **Task 7: Tích hợp Worker & Endpoints API Giám sát Biến thiên Điểm chuẩn Động**

### SPRINT 5: LƯU THẬT TRI THỨC CHATBOT & BẢO VỆ RANH GIỚI DỰ BÁO AI (Hoàn thành 100%)
- [x] **Task 1: Hoàn thiện CRUD Tri thức Chatbot kết nối CSDL Supabase thật (`/api/chat/knowledge`)**
- [x] **Task 2: Cơ chế Tự động Đồng bộ & Tải lại Bộ nhớ RAM RAG BM25 tức thì sau khi Thêm/Sửa/Xóa Tri thức**
- [x] **Task 3: Bảo mật Phân quyền Admin Quản lý Tri thức (`verify_internal_api_key`)**
- [x] **Task 4: Phân định Ranh giới Nghiệp vụ: Tuyệt đối không dùng Dự báo AI làm Kết quả Trúng tuyển Chính thức**

### SPRINT 6: ĐÓNG BĂNG MÃ NGUỒN AI, KIỂM THỬ HỒI QUY XUYÊN LUỒNG & BACKLOG MÔ HÌNH
- [x] **Task 1: Đóng băng Mã nguồn Backend AI (Zero Modification to Stable AI Core)**
- [x] **Task 2: Duy trì Bộ Kiểm thử Hồi quy Toàn diện (Full Regression Test Suite - 226/226 Tests Pass 100%)**
- [x] **Task 3: Tương thích Hai chiều Frontend (Bidirectional Compatibility Layer cho Chatbot, MBTI và Prediction)**
- [ ] **Task 4 (Backlog Dài hạn sau Sprint 6): Hệ thống Ghi nhận Phản hồi & Đánh giá Chất lượng Mô hình (Model Evaluation & User Feedback Tracking)**

---

# =====================================================================
# SPRINT 1: CORE PLATFORM, MBTI & AI CHATBOT [HOÀN THÀNH 100%]
# =====================================================================

### GIAI ĐOẠN 1: NỀN TẢNG CORE & MÔI TRƯỜNG MICROSERVICE
> **Mục tiêu**: Thiết lập môi trường chạy độc lập, cấu hình FastAPI, xử lý CORS và quản lý lỗi tập trung.

- [x] **Task 1.1: Khởi tạo danh sách thư viện phụ thuộc (`requirements.txt`)**
  - Khai báo các thư viện thiết yếu: `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `python-dotenv`, `httpx`, `numpy`, `psycopg2-binary`.
- [x] **Task 1.2: Triển khai cấu hình hệ thống (`src/core/config.py`)**
  - Xây dựng class `Settings` quản lý biến môi trường: `DATABASE_URL`, `DIRECT_URL`, `CORS_ORIGINS`, `NVIDIA_API_KEY`.
- [x] **Task 1.3: Xây dựng cơ chế bắt lỗi tập trung (`src/core/exceptions.py`)**
  - Bắt lỗi thống nhất, trả về format JSON chuẩn (`success: false, error: ...`).
- [x] **Task 1.4: Cấu hình bảo mật & Middleware (`src/core/security.py`)**
  - Cấu hình CORS middleware cho phép kết nối từ `http://localhost:3000`.
- [x] **Task 1.5: Khởi tạo FastAPI Server (`app.py`)**
  - Khởi tạo app FastAPI, include router, endpoint kiểm tra sức khỏe `GET /health`.

---

### GIAI ĐOẠN 2: MODULE MBTI (TRẮC NGHIỆM TÍNH CÁCH & GỢI Ý NGÀNH UTC)
> **Mục tiêu**: Cung cấp API bộ câu hỏi trắc nghiệm MBTI, tính điểm 4 trục tính cách và đề xuất top ngành học UTC.

- [x] **Task 2.1: Xây dựng Schemas cho MBTI (`src/schemas/mbti_schema.py`)**
  - `MBTIQuestionListResponse`, `MBTISubmitRequest` (hỗ trợ cả dict và list answers, camelCase/snake_case), `MBTIResultResponse`.
- [x] **Task 2.2: Thuật toán chấm điểm và ánh xạ ngành UTC (`src/ml/mbti/scorer.py`)**
  - Tính điểm 4 trục (E/I, S/N, T/F, J/P), từ điển 16 nhóm tính cách gắn với các ngành đào tạo thực tế tại UTC.
- [x] **Task 2.3: Xử lý nghiệp vụ & Tích hợp CSDL (`src/services/mbti_service.py`, `src/repositories/major_repository.py`)**
  - Nạp danh mục 69 ngành đào tạo từ Supabase PostgreSQL vào bộ nhớ cache.
  - Sinh báo cáo phân tích hướng nghiệp cơ bản và top ngành phù hợp.
- [x] **Task 2.4: Tạo các Endpoint MBTI Router (`src/router/mbti_router.py`)**
  - `GET /api/mbti/questions`: Lấy 20 câu hỏi trắc nghiệm chuẩn.
  - `POST /api/mbti/submit`: Chấm điểm và trả về kết quả phân tích MBTI.

---

### GIAI ĐOẠN 3: MODULE LLM & RAG CHATBOT (HỎI ĐÁP AI & QUẢN LÝ DỮ LIỆU HUẤN LUYỆN)
*(Chuyển từ Giai đoạn 4 cũ sang)*
> **Mục tiêu**: Xây dựng trợ lý AI tư vấn tuyển sinh UTC 24/7 và hệ thống CRUD quản lý tri thức RAG kết nối Supabase.

- [x] **Task 3.1: Xây dựng Schemas Chatbot & Quản lý tri thức (`src/schemas/chat_schema.py`)**
  - `ChatRequest`, `ChatResponse` (kèm `sources`, `suggested_questions`), `KnowledgeItemSchema` (hỗ trợ trường song ngữ DB/Frontend).
- [x] **Task 3.2: Tích hợp 124 Chunks từ Sổ tay K67 & Niên giám K64 (`src/ml/llm/knowledge/`)**
  - Nạp 81 chunks Sổ tay K67 và 43 chunks Niên giám K64 về quy chế, tín chỉ, chuẩn đầu ra, việc làm.
- [x] **Task 3.3: Thiết kế Prompt Engineering Cố vấn Tuyển sinh UTC (`src/ml/llm/prompt_templates.py`)**
  - System Prompt chuẩn mực vai trò chuyên viên tư vấn UTC, trích dẫn tài liệu chính xác, trả lời bằng tiếng Việt.
- [x] **Task 3.4: Xây dựng RAG Engine BM25 tiếng Việt (`src/ml/llm/rag.py`)**
  - Tách từ đơn/kép (unigram + bigram), tìm kiếm kết hợp đa nguồn từ file và 132 mục tri thức thực tế từ Supabase.
- [x] **Task 3.5: Repository & Service Chatbot (`src/repositories/chat_repository.py`, `src/services/chat_service.py`)**
  - Tích hợp NVIDIA LLaMA 3.2 11B Vision Instruct, cơ chế dự phòng an toàn (fallback) khi mạng chậm.
  - Full CRUD cho tri thức và hàm đồng bộ tức thì (`sync_knowledge`).
- [x] **Task 3.6: Xây dựng Router Endpoints (`src/router/chat_router.py`)**
  - `POST /api/chat`: Hỏi đáp AI Chatbot.
  - `GET /api/chat/knowledge`: Lấy danh sách tri thức.
  - `POST /api/chat/knowledge`: Thêm tri thức mới (tự động re-index RAG RAM).
  - `PUT /api/chat/knowledge/{id}`: Sửa tri thức (tự động re-index RAG RAM).
  - `DELETE /api/chat/knowledge/{id}`: Xóa tri thức (tự động re-index RAG RAM).
  - `POST /api/chat/sync-knowledge`: Đồng bộ lại toàn bộ dữ liệu CSDL vào bộ nhớ RAG.

---

# =====================================================================
# SPRINT 2: TƯ VẤN HƯỚNG NGHIỆP, DỰ ĐOÁN ĐIỂM CHUẨN & XÁC SUẤT TRÚNG TUYỂN
# =====================================================================

### TASK 1 (SPRINT 2): XEM KẾT QUẢ TƯ VẤN HƯỚNG NGHIỆP
> **Mục tiêu**: Hoàn thiện vòng đời trải nghiệm hướng nghiệp: Lưu trữ kết quả vào CSDL, cung cấp báo cáo phân tích chuyên sâu đa chiều, và cho phép tra cứu lại lịch sử trắc nghiệm.

- [x] **Task 2.1.1: Mở rộng Schemas Báo cáo Hướng nghiệp Nâng cao (`src/schemas/mbti_schema.py`)**
  - Bổ sung cấu trúc dữ liệu cho báo cáo chuyên sâu:
    - `personality_traits`: Phân tích chi tiết điểm mạnh (Strengths), điểm cần cải thiện (Weaknesses), phong cách làm việc nhóm & khả năng lãnh đạo.
    - `academic_environment`: Môi trường giảng đường phù hợp (thực hành xưởng, đồ án nhóm, nghiên cứu lý thuyết).
    - `career_trajectories`: Bản đồ lộ trình nghề nghiệp tương ứng cho từng ngành đề xuất (Ví dụ: Kỹ sư phần mềm, Kiến trúc sư giải pháp, Quản trị Logistics, Kỹ sư cầu đường...).
    - `major_details`: Thông tin mở rộng về ngành học UTC (Khoa viện, loại bằng cấp/chuẩn đầu ra CDIO, học phí ước tính/kỳ, cơ hội học bổng & việc làm).
  - `MBTIHistoryResponse`: Schema danh sách lịch sử các lần làm bài của thí sinh theo `session_id` hoặc `cccd`.

- [x] **Task 2.1.2: Lưu trữ kết quả trắc nghiệm vào CSDL Supabase (`src/repositories/mbti_repository.py`)**
  - Tạo mới `MBTI_Repository` kết nối bảng `ket_qua_trac_nghiem`:
    - `save_result(session_id, cccd, nhom_tinh_cach, goi_y_nganh, thoi_gian_thuc_hien)`: Tự động lưu bản ghi khi thí sinh submit.
    - `get_result_by_id(ma_ket_qua)`: Lấy thông tin bài làm để hiển thị lại theo ID.
    - `get_history_by_session(session_id)`: Lấy danh sách các lần làm trắc nghiệm trong phiên truy cập.

- [x] **Task 2.1.3: Xây dựng Service Hướng nghiệp Chuyên sâu (`src/services/mbti_service.py`)**
  - Cải tiến logic phân tích: Kết hợp thông tin từ Niên giám K64 để sinh phân tích định hướng nghề nghiệp chuẩn UTC.
  - Cung cấp tính năng tra cứu lại kết quả đã lưu mà không cần làm lại bài.

- [x] **Task 2.1.4: Mở rộng Endpoints tại MBTI Router (`src/router/mbti_router.py`)**
  - `GET /api/mbti/result/{result_id}`: Xem chi tiết báo cáo tư vấn hướng nghiệp theo mã kết quả.
  - `GET /api/mbti/history`: Tra cứu lịch sử kết quả theo `session_id` hoặc `cccd`.
  - Cập nhật `POST /api/mbti/submit`: Lưu tự động vào CSDL và trả về `result_id` để FE điều hướng sang trang kết quả `/trac-nghiem-mbti/ket-qua?id=...`.

---

### TASK 2 (SPRINT 2): DỰ ĐOÁN ĐIỂM CHUẨN NGÀNH HỌC (HYBRID SIMULATION & ROBUST ML)
> **Mục tiêu**: Dự báo điểm chuẩn tuyển sinh năm 2026 và mở rộng cho năm 2027 cho toàn bộ **54 chương trình đào tạo Cơ sở Hà Nội (`GHA`)**, kết hợp giữa mô phỏng ngược cơ chế thị trường lọc ảo (Gale-Shapley / Deferred Acceptance) và mô hình học máy kháng nhiễu (Huber Regressor), đồng thời áp dụng chuẩn quy đổi điểm tương đương 4 phương thức của Bộ GD&ĐT (PT1, PT2, PT3, PT4).

- [x] **Task 2.2.1: Thu thập & Chuẩn hóa Dữ liệu Tuyển sinh Cơ sở Hà Nội (`GHA`)**
  - Giới hạn phân vùng: Tập trung chuyên biệt **54 ngành Cơ sở Hà Nội (`GHA01` - `GHA33`)**, loại bỏ triệt để phân hiệu TP.HCM (`GSA`) khỏi tập huấn luyện.
  - Xây dựng mỏ neo 2025: Trích xuất chỉ tiêu, điểm chuẩn thực tế các phương thức và tổ hợp môn (`ml_simulation/data/extracted/hanoi_anchor_2025_2026.json`).
  - Thu thập dữ liệu vĩ mô: 24 biểu đồ phổ điểm THPT toàn quốc, phổ điểm HSA ĐHQGHN, TSA ĐHBK Hà Nội, và ma trận tương quan THPT - Học bạ theo Phụ lục III Bộ GD&ĐT.

- [x] **Task 2.2.2: Động cơ Mô phỏng Ngược Cơ chế Tuyển sinh (Reverse Generative Simulation)**
  - Thuật toán sinh điểm: Phân phối Beta cắt cụt, chiết khấu điểm ưu tiên thí sinh đạt $>22.5$ điểm, phân rã tổ hợp 3 môn có tương quan thực tế (`score_sampler.py`).
  - Quần thể thí sinh ảo: Sinh **16.162 thí sinh ảo** tạo ra **46.826 lượt nguyện vọng**, khớp đúng **tỉ lệ chọi thực tế 10.0 : 1** (khoảng 1:9 đến 1:12) của UTC (`reverse_simulator.py`).
  - Cơ chế hành vi: Phân cụm Markov theo 5 nhóm ngành (IT/CS, Cơ khí - Ô tô, Điện - Tự động hóa, Kinh tế - Vận tải, Xây dựng - Hạ tầng) và mô phỏng cơ chế Top-tier Drainage (thoát điểm sang Bách Khoa/ĐHQG).
  - Thuật toán lọc ảo Gale-Shapley (Deferred Acceptance): Khớp nguyện vọng lặp hội tụ đạt sai số $MAE = 0.703$ điểm trên mỏ neo 2025.

- [x] **Task 2.2.3: Thử nghiệm, Đối chuẩn 7 Mô hình ML & Đóng gói Model Checkpoint**
  - Đánh giá 5-Fold Cross Validation trên 54 ngành Hà Nội (`ml_comparison.py`):
    - **Huber Regressor**: $MAE = 0.583$ đ, $RMSE = 0.778$, $R = 0.899$, $79.6\%$ ngành sai số $\le 1.0$ đ (Xếp hạng 1 - Khuyên dùng).
    - **Ridge Regression**: $MAE = 0.593$ đ, $RMSE = 0.774$, $R = 0.897$ (Xếp hạng 2).
    - ElasticNet ($MAE = 0.738$), Hybrid Stacking ($MAE = 0.781$), GBDT ($MAE = 0.815$), Random Forest ($MAE = 0.880$), Gale-Shapley Baseline ($MAE = 0.995$).
  - Lưu trữ kết quả đối chuẩn: Toàn bộ dữ liệu 7 mô hình được bảo toàn tại `model_comparison_results.json`.
  - Đóng gói model nhị phân: Xuất file trọng số `ml_simulation/models/huber_regressor_2026.joblib` và `model_metadata.json` sẵn sàng phục vụ suy luận (Inference).

- [x] **Task 2.2.4: Động cơ Quy đổi Tương đương 4 Phương thức Tuyển sinh 2026**
  - Tích hợp Bảng quy đổi điểm tuyển sinh chính thức năm 2026 của Bộ GD&ĐT (`conversion_scales_2026.json`).
  - Nội suy tuyến tính từng khoảng: Quy đổi từ điểm THPT (thang 30) sang Học bạ PT2 (thang 30), ĐGNL HSA PT3 (thang 150), ĐGTD TSA PT4 (thang 100).
  - Xuất bảng đầy đủ 54 ngành: `ml_simulation/FULL_MAJORS_TABLE.md` và `full_54_majors_table.json`.

- [x] **Task 2.2.5: Thiết kế Pipeline Tự động Hóa cho Mùa Tuyển sinh 2027**
  - Xây dựng module tự vận hành: `ml_simulation/pipeline_2027.py`.
  - Cơ chế lăn bánh (Rolling forecast): Tự động nạp chỉ tiêu $Q_{2027}$ và độ lệch phổ điểm $\Delta Phổ\_điểm_{2027}$ để xuất trọn gói điểm chuẩn dự báo năm 2027 mà không cần viết lại mã nguồn hay huấn luyện lại từ đầu.

- [x] **Task 2.2.6: Tích hợp Dữ liệu Dự báo Điểm chuẩn vào CSDL Supabase (`du_doan_diem_chuan`)**
  - Đã nạp thành công 54 bản ghi điểm chuẩn dự báo năm 2026 từ mô hình Huber ML vào bảng `du_doan_diem_chuan`.
  - Khóa ngoại tham chiếu chính xác 100% đến `chuong_trinh_dao_tao(ma_chuong_trinh)`.

- [x] **Task 2.2.7: Xây dựng Schemas Dự đoán Điểm chuẩn (`src/schemas/prediction_schema.py`)** *(Hoàn thành: Bổ sung trường điểm động và tin tức xu hướng)*
  - `BenchmarkAnchorItem`: Điểm mỏ neo chuẩn năm 2025 và chỉ tiêu của chương trình đào tạo.
  - `BenchmarkPredictionRequest`: Mã chương trình (`ma_chuong_trinh`), phương thức xét tuyển (`PT1`, `PT2`, `PT3`, `PT4`).
  - `BenchmarkPredictionResponse`: Điểm mỏ neo 2025, điểm chuẩn dự báo 2026 kỳ vọng, khoảng dao động tin cậy $[Min, Max]$, xu hướng biến động (`TĂNG`, `GIẢM`, `ỔN_ĐỊNH`), điểm tương đương 4 phương thức (PT1 THPT, PT2 Học bạ, PT3 HSA, PT4 TSA), và các nhân tố ảnh hưởng.
  - `BenchmarkScenarioRequest`: Tham số giả lập kịch bản tuyển sinh (chỉ tiêu tùy biến, độ lệch phổ điểm giả định).

- [x] **Task 2.2.8: Xây dựng Repository & Service Dự báo Điểm chuẩn (`src/repositories/prediction_repository.py`, `src/services/prediction_service.py`)** *(Hoàn thành: Nâng cấp suy luận Bayes động & Cold-start)*
  - `PredictionRepository`: Truy vấn dữ liệu mỏ neo năm 2025 và kết quả dự báo điểm chuẩn 2026 từ bảng `du_doan_diem_chuan` (hoàn toàn không sử dụng hay truy vấn dữ liệu trước năm 2025).
  - `PredictionService`: Load checkpoint mô hình `huber_regressor_2026.joblib` để thực hiện suy luận động khi giả lập kịch bản hoặc lấy kết quả đã lưu; áp dụng bộ quy đổi 4 phương thức chuẩn Bộ GD&ĐT.

- [x] **Task 2.2.9: Xây dựng Endpoints Router Dự đoán Điểm chuẩn (`src/router/prediction_router.py`)** *(Hoàn thành: Thêm tham số theo dõi theo mốc thời gian & Cold-start)*
  - `GET /api/predict/benchmark/{ma_chuong_trinh}`: Xem chi tiết điểm chuẩn dự báo 2026 đối sánh với mỏ neo 2025 kèm quy đổi 4 phương thức cho một ngành cụ thể.
  - `GET /api/predict/all-benchmarks`: Lấy danh sách điểm chuẩn dự báo toàn bộ 54 ngành Cơ sở Hà Nội năm 2026.
  - `POST /api/predict/simulate-scenario`: Giả lập kịch bản dự báo khi người dùng điều chỉnh chỉ tiêu hoặc phổ điểm.

---

### TASK 3 (SPRINT 2): DỰ ĐOÁN KHẢ NĂNG TRÚNG TUYỂN [HOÀN THÀNH 100%]
> **Mục tiêu**: Đánh giá định lượng xác suất đỗ của thí sinh vào các ngành của UTC dựa trên điểm học tập, tổ hợp môn, điểm ưu tiên và đưa ra chiến lược sắp xếp nguyện vọng thông minh theo phân phối động.

- [x] **Task 2.3.1: Xây dựng Schemas Đánh giá Khả năng Trúng tuyển (`src/schemas/prediction_schema.py`)**
  - `AdmissionChanceRequest`:
    - `academic_scores`: Điểm các môn (Toán, Lý, Hóa, Văn, Anh, Sinh, Tin...) theo điểm thi tốt nghiệp hoặc học bạ THPT. Đã tích hợp bộ kiểm tra chặn phạm vi [0.0, 10.0].
    - `target_major_code`: Mã ngành mong muốn xét tuyển (hoặc để trống để quét toàn bộ ngành).
    - `admission_method`: Phương thức xét tuyển (`PT1`: Điểm thi THPT, `PT2`: Học bạ, `PT3`: ĐGNL/ĐGTD).
    - `priority_region`: Khu vực ưu tiên (`KV1`, `KV2_NT`, `KV2`, `KV3`).
    - `priority_group`: Đối tượng ưu tiên (`DT_01` -> `DT_07` hoặc không).
    - `foreign_language_cert`: Chứng chỉ ngoại ngữ nếu có (IELTS, TOEFL, JLPT...).
  - `AdmissionChanceResponse`:
    - `calculated_score`: Điểm xét tuyển chính thức sau khi cộng điểm ưu tiên & quy đổi ngoại ngữ.
    - `admission_probability`: Xác suất trúng tuyển (0% - 100%).
    - `risk_level`: Phân loại mức độ an toàn (`SAFE`: An toàn, `TARGET`: Vừa sức, `REACH`: Thử thách, `HIGH_RISK`: Rủi ro).
    - `gap_score`: Độ chênh lệch giữa điểm thí sinh và điểm chuẩn dự kiến ($\Delta = Điểm - Chuẩn$).
    - `advice`: Lời khuyên tư vấn tuyển sinh cụ thể từ chuyên gia UTC.
  - `MajorRecommendationResponse`: Bảng phân loại toàn bộ 35+ ngành học UTC theo 3 giỏ:
    - Giỏ An toàn (Xác suất > 85%).
    - Giỏ Vừa sức (Xác suất 65% - 85%).
    - Giỏ Mạo hiểm / Thử thách (Xác suất 40% - 65%).

- [x] **Task 2.3.2: Bộ máy Tính điểm Quy đổi & Ưu tiên (`src/ml/prediction/admission_predictor.py`)**
  - Cài đặt công thức tính điểm ưu tiên chuẩn Thông tư Bộ GD&ĐT:
    - Nếu Tổng điểm $\ge 22.5$: Giảm trừ mức ưu tiên theo công thức: $\text{Ưu tiên} = \frac{30 - \text{Tổng điểm}}{7.5} \times \text{Mức chuẩn}$.
  - Cài đặt bảng quy đổi chứng chỉ IELTS/TOEFL sang thang điểm 10 môn Tiếng Anh theo Đề án tuyển sinh UTC 2026.
  - Tự động chọn tổ hợp môn tối ưu nhất (Điểm cao nhất) cho từng ngành nếu thí sinh cung cấp nhiều môn.

- [x] **Task 2.3.3: Thuật toán Đánh giá Xác suất Trúng tuyển (`src/ml/prediction/admission_predictor.py`)**
  - Mô hình xác suất dựa trên hàm Phân phối tích lũy chuẩn (Gaussian Cumulative Distribution Function) và hàm Sigmoid:
    $$P(\text{Trúng tuyển}) = \frac{1}{1 + e^{-k \cdot (Score_{thí sinh} - Score_{chuẩn dự kiến})}}$$
  - Tham số độ dốc $k$ được căn chỉnh dựa trên độ phân tán phổ điểm lịch sử của từng khối thi (A00, A01, D01...).

- [x] **Task 2.3.4: Thuật toán Tư vấn Chiến lược Nguyện vọng Thông minh**
  - Sinh chiến lược đặt nguyện vọng theo quy tắc "Kim tự tháp an toàn":
    - NV1 - NV2: Nguyện vọng ước mơ (Nhóm Thử thách).
    - NV3 - NV4: Nguyện vọng trọng tâm (Nhóm Vừa sức).
    - NV5+: Nguyện vọng bảo hiểm tuyệt đối (Nhóm An toàn).

- [x] **Task 2.3.5: Xây dựng Endpoints Đánh giá Trúng tuyển (`src/router/prediction_router.py`)**
  - `POST /api/predict/admission-chance`: Đánh giá xác suất đỗ vào 1 ngành cụ thể.
  - `POST /api/predict/recommend-majors`: Quét toàn trường và đề xuất danh sách ngành theo 3 nhóm rủi ro kèm chiến lược đặt nguyện vọng.

---

### TASK 4 (SPRINT 2): TẦNG LƯU TRỮ VÀ NHẬT KÝ DỰ ĐOÁN [HOÀN THÀNH 100%]
> **Mục tiêu**: Định nghĩa entities tầng models, map kết quả trắc nghiệm và tính toán dự đoán realtime on-the-fly theo yêu cầu.

- [x] **Task 2.4.1: Định nghĩa Entities / Models (`src/models/`)**
  - `src/models/mbti_result.py`: Mô hình kết quả trắc nghiệm map với bảng `ket_qua_trac_nghiem`.
  - `src/models/prediction_log.py`: Mô hình thực thể đánh giá dự đoán điểm và khả năng trúng tuyển (In-memory DTO / realtime model).
  - `src/models/chat_history.py`: Mô hình lịch sử chat hội thoại.
- [x] **Task 2.4.2: Tầng Repository xử lý truy xuất và nhật ký (`src/repositories/prediction_repository.py`)**
  - Tính toán realtime on-the-fly theo yêu cầu, không ghi rác vào CSDL quan hệ chung; theo dõi phiên đánh giá in-memory.

---

### TASK 5 (SPRINT 2): KIỂM THỬ TÍCH HỢP, TỐI ƯU HÓA & KẾT NỐI FRONTEND [HOÀN THÀNH 100%]
> **Mục tiêu**: Đảm bảo toàn bộ các module của Sprint 2 hoạt động chính xác, hiệu năng cao và tương thích giao diện người dùng.

- [x] **Task 2.5.1: Viết Unit Test và TestClient cho toàn bộ API Sprint 2**
  - Đầy đủ test suite kiểm thử toàn diện toàn bộ 23 endpoints, repositories, services với 215/215 test cases Pass 100%.
- [x] **Task 2.5.2: Kiểm tra tính toán biên, Edge Cases & Tiền kiểm tra dữ liệu**
  - Xử lý các ca điểm đặc thù: Điểm chạm sàn (0.0), điểm trần (10.0 môn học, 30/30 tổ hợp), điểm sát mốc 22.5, điểm ưu tiên tiệm cận 30.
  - Chặn nghiêm ngặt dải điểm môn học trong khoảng [0.0, 10.0] tại tầng DTO Pydantic (`AdmissionChanceRequest`), từ chối điểm âm (-1) và điểm vượt trần (11) với mã lỗi 422.
- [x] **Task 2.5.3: Cập nhật tài liệu bàn giao API & Kết nối Frontend**
  - Lập tài liệu bàn giao chi tiết `FRONTEND_INTEGRATION_HANDOVER.md` cho các trang giao diện `/tinh-diem-quy-doi`, `/trac-nghiem-mbti`, `/hoi-dap-ai`.

---

# =====================================================================
# SPRINT 3: HỆ THỐNG DỰ ĐOÁN ĐIỂM ĐỘNG REAL-TIME & THUẬT TOÁN COLD-START 2027 [HOÀN THÀNH 100%]
# =====================================================================

### TASK 1 (SPRINT 3): CƠ CHẾ DỰ BÁO ĐIỂM CHUẨN ĐỘNG LIÊN TỤC (REAL-TIME DYNAMIC CUTOFF UPDATING)
> **Mục tiêu**: Thay thế mô hình dự báo tĩnh một lần bằng cơ chế suy luận Bayes cập nhật liên tục từ thời điểm mở cổng tuyển sinh sớm (Học bạ PT2, ĐGNL HSA, ĐGTD TSA) đến khi chốt cổng THPT.

- [x] **Task 3.1.1: Thiết kế Pipeline Suy luận Bayes Động (Bayesian Updating Engine)**
  - Tách điểm dự đoán thành 2 thành phần: Điểm Tiên nghiệm (Prior ML: $S_0$ từ Huber Regressor + Lịch sử) và Bằng chứng Thực tế (Evidence: $S_{\text{thực tế}}(t)$ từ hồ sơ đã nộp).
  - Cài đặt hàm trọng số biến thiên theo thời gian: $w(t) = \frac{N(t)}{N(t) + K_0}$ để làm mịn, tránh nhiễu điểm số khi số lượng hồ sơ ban đầu còn ít.
- [x] **Task 3.1.2: Mô hình Ngoại suy Đường cong Nộp hồ sơ Chữ S (Logistic Influx Curve & KDE)**
  - Đo lường tốc độ nộp hồ sơ $\Delta N / \Delta t$ theo từng ngành học.
  - Áp dụng mô hình Kernel Density Estimation (KDE) ngoại suy phân phối điểm của toàn bộ tập thí sinh cuối cùng $N_{\text{final}}$ để xác định ngưỡng cắt thứ $K$ (chỉ tiêu).
- [x] **Task 3.1.3: Bộ Lọc Ảo Đa Phương Thức (Virtual Candidate Filtering)**
  - Gán trọng số xác nhận nhập học (Commitment Weight) theo thứ tự nguyện vọng của thí sinh (NV1: 1.0, NV2: 0.7, NV3+: 0.35) để loại bỏ hiện tượng điểm ảo khi thí sinh nộp nhiều phương thức/nhiều trường.

---

### TASK 2 (SPRINT 3): MODULE PHÂN TÍCH TIN TỨC & XU HƯỚNG XÃ HỘI TÁC ĐỘNG ĐIỂM CHUẨN (MARKET TREND & NEWS IMPACT ENGINE)
> **Mục tiêu**: Theo dõi và định lượng tác động của tin tức truyền thông, thị trường lao động (ví dụ: AI ảnh hưởng ngành CNTT khiến điểm giảm, làn sóng đầu tư hạ tầng giúp Xây dựng/Giao thông tăng điểm) vào mô hình dự đoán.

- [x] **Task 3.2.1: Bộ thu thập Tin tức Tự động Đa nguồn (Auto News Aggregator & Crawler)**
  - Tích hợp luồng Google News RSS tự động truy vấn theo từ khóa chuyên ngành (`"việc làm công nghệ thông tin"`, `"đường sắt tốc độ cao bắc nam"`, `"nhân lực vi mạch bán dẫn"`, `"điểm chuẩn đại học"`...).
  - Kết nối luồng RSS chính thức từ các chuyên mục Giáo dục & Lao động Việc làm của các báo lớn (VnExpress, Dân Trí, Tuổi Trẻ, Cổng thông tin Bộ GD&ĐT).
  - Cài đặt bộ lọc từ khóa sơ bộ (Keyword Whitelist Pre-filter) để tự động loại bỏ 90% tin tức rác trước khi gửi sang LLM, tối ưu tài nguyên và chi phí token.
  - Hỗ trợ giao diện cho Ban tuyển sinh dán link hoặc nhập bài viết quan trọng thủ công.
- [x] **Task 3.2.2: Trích xuất Thực thể & Phân tích Cảm xúc bằng LLM (Entity Linking & Sentiment Analysis)**
  - Tận dụng LLaMA 3.2 11B phân tích nội dung bài báo, tự động ánh xạ bài viết đến 69 ngành UTC hoặc nhóm ngành tương ứng (`IT_CS`, `CIVIL_CONSTRUCTION`, `RAILWAY`, `ECONOMICS`, `LOGISTICS`, `ENGLISH`...).
  - Chấm điểm cảm xúc và cường độ tác động thị trường: Phân loại theo dải $[-1.0, +1.0]$ (`TÍCH_CỰC`, `TIÊU_CỰC`, `TRUNG_TÍNH`).
- [x] **Task 3.2.3: Mô hình hóa Hệ số Xu hướng Thị trường có Suy giảm Thời gian (Time-decay Trend Multiplier $\Delta_{\text{news}}$)**
  - Xây dựng công thức tổng hợp điểm xu hướng: $\Delta_{\text{news}}(k) = \sum \text{Sentiment}_i \cdot \text{Credibility}_i \cdot e^{-\lambda (t - t_i)}$ để ưu tiên tin tức mới nhất.
  - Tích hợp trọng số $\Delta_{\text{news}}$ vào mô hình hồi quy Huber Regressor và bộ lọc Bayes với hệ số co cụm (Shrinkage factor $\alpha \approx 0.4$) để kiểm soát biên độ biến động hợp lý ($\le \pm 0.8$ điểm).
- [x] **Task 3.2.4: Module Giải thích Minh bạch (Explainable AI - XAI Trend Insights)**
  - Trả về trường `trend_insights` trong API dự đoán, trích dẫn bài báo và luận điểm cụ thể cho thí sinh (ví dụ: *"Ngành CNTT dự báo giảm 0.4đ do tâm lý thị trường lo ngại tác động của Generative AI theo các báo cáo việc làm gần nhất..."*).
- [x] **Task 3.2.5: Giao diện Quản trị & Hiệu chỉnh Trọng số Tin tức cho Admin**
  - Cung cấp CRUD API cho phép Admin kiểm duyệt tin tức đã quét, điều chỉnh hệ số tác động hoặc loại bỏ tin tức rác trước khi đưa vào mô hình dự báo.

---

### TASK 3 (SPRINT 3): THUẬT TOÁN COLD-START CHO MÔN THI MỚI NĂM 2027
> **Mục tiêu**: Xử lý kịch bản Bộ GD&ĐT bổ sung môn thi mới vào kỳ thi tốt nghiệp THPT (ví dụ: Tin học, Công nghệ) chưa từng có dữ liệu điểm thi trong quá khứ.

- [x] **Task 3.3.1: Mô hình Quy đổi Phân vị Tương đương Toàn quốc (Percentile Equating / Quantile Matching)**
  - Thu thập và chuẩn hóa phân phối tích lũy xác suất (CDF) của môn thi mới dựa trên công bố phổ điểm toàn quốc của Bộ GD&ĐT.
  - Ánh xạ điểm thô môn mới sang phân vị tương đương ($\text{Percentile}(x)$), chuyển đổi về điểm chuẩn hóa z-score: $z = \frac{x - \mu}{\sigma}$.
- [x] **Task 3.3.2: Tích hợp Tổ hợp Mới vào Ma trận Equating của Bộ máy Dự đoán**
  - Tự động thay thế/bổ sung môn thi mới vào các tổ hợp hiện có (như X06: Toán - Lý - Tin) mà không làm suy giảm độ chính xác của bộ hồi quy Huber Regressor.

---

### TASK 4 (SPRINT 3): THUẬT TOÁN COLD-START CHO NGÀNH HỌC MỚI MỞ NĂM 2027
> **Mục tiêu**: Ước lượng điểm chuẩn và khả năng trúng tuyển cho các ngành đào tạo mới mở hoàn toàn (ví dụ: Kỹ thuật Đường sắt Tốc độ cao, Vi mạch Bán dẫn, AI Y sinh) chưa có điểm sàn năm trước.

- [x] **Task 3.4.1: Mô hình Học chuyển giao Cụm ngành Tương đồng (Cross-Major Transfer Learning & KNN)**
  - Xây dựng ma trận đặc trưng không gian ngành (Khối kiến thức, Khoa quản lý, Thời lượng đào tạo Cử nhân/Kỹ sư, Mức học phí).
  - Tìm kiếm k-ngành lân cận gần nhất (K-Nearest Neighbors) trong CSDL UTC để chuyển giao mỏ neo điểm chuẩn cơ sở.
- [x] **Task 3.4.2: Tham chiếu Mỏ neo Ngoại suy Liên trường (Cross-University Benchmarking)**
  - Cho phép nạp dữ liệu tham chiếu từ các trường đại học khối kỹ thuật tương đương (Bách Khoa, ĐHQG) kết hợp hệ số hiệu chỉnh vị thế thương hiệu UTC.

---

### TASK 5 (SPRINT 3): KHAI THÁC DỮ LIỆU HÀNH VI SỚM & KHOẢNG TIN CẬY ĐỘNG
> **Mục tiêu**: Thu thập tín hiệu quan tâm của thí sinh trước mùa tuyển sinh và hiển thị độ bất định minh bạch cho người dùng.

- [x] **Task 3.5.1: Bộ thu thập Tín hiệu Hành vi Sớm (Behavioral Telemetry Cold-Start)**
  - Tổng hợp tần suất thí sinh làm trắc nghiệm MBTI hướng tới ngành mới, số lượt tra cứu ngành và số lượt chạy thử tính điểm quy đổi.
  - Tính toán chỉ số "Tốc độ Quan tâm" (Interest Velocity) để điều chỉnh biên độ cạnh tranh $\Delta_{\text{trend}}$ của ngành mới.
- [x] **Task 3.5.2: Đánh giá Độ bất định & Khoảng Tin cậy Động (Uncertainty Estimation)**
  - Tự động mở rộng khoảng tin cậy cho ngành mới / môn mới ($[S \pm 1.0]$ so với $[S \pm 0.35]$ của ngành truyền thống).
  - Trả về trường `confidence_level: LOW_COLD_START` kèm thông điệp khuyến nghị chiến lược an toàn cho thí sinh.

---

### TASK 6 (SPRINT 3): WORKER ĐỊNH KỲ & API GIÁM SÁT ĐIỂM CHUẨN ĐỘNG
> **Mục tiêu**: Tự động hóa quá trình tính toán và cung cấp endpoint cho ban tuyển sinh theo dõi biến động điểm theo thời gian thực.

- [x] **Task 3.6.1: Scheduled Worker / Background Task Cập nhật Điểm chu kỳ**
  - Thiết lập cron worker quét định kỳ (mỗi 1 giờ / 6 giờ) bảng `nguyen_vong_sinh_vien`, kích hoạt tính toán điểm chuẩn động và cập nhật cache RAM.
- [x] **Task 3.6.2: Endpoints API Giám sát Xu hướng Biến thiên Điểm chuẩn**
  - `GET /api/predict/dynamic-trends/{ma_chuong_trinh}`: Lấy lịch sử biến thiên điểm chuẩn dự báo theo từng ngày từ khi mở cổng đến hiện tại.
  - `POST /api/predict/cold-start/configure-major`: Cung cấp giao diện API cho Admin thiết lập thông số tương đồng khi mở ngành đào tạo mới.
  - `POST /api/predict/cold-start/percentile-equating`: Cung cấp API quy đổi phân vị môn thi mới 2027 sang thang điểm tham chiếu.


---

# =====================================================================
# SPRINT 5: LƯU THẬT TRI THỨC CHATBOT & BẢO VỆ RANH GIỚI DỰ BÁO AI [HOÀN THÀNH 100%]
# =====================================================================
> **Đối chiếu SPRINT-5-TOI-THIEU.md**: Triển khai lưu thật kho dữ liệu tri thức huấn luyện Chatbot AI, hỗ trợ form Admin Next.js và đảm bảo ranh giới dữ liệu dự báo.

### TASK 1 (SPRINT 5): HOÀN THIỆN CRUD TRI THỨC KẾT NỐI BẢNG `tri_thuc_ai` TRÊN SUPABASE
> **Mục tiêu**: Thay thế toàn bộ mock memory bằng kết nối trực tiếp CSDL PostgreSQL/Supabase thật cho 132 mục tri thức tuyển sinh.
- [x] **Task 5.1.1: Tầng Repository Tri thức AI (`src/repositories/chat_repository.py`)**
  - Kết nối trực tiếp bảng `tri_thuc_ai`, hỗ trợ phân trang, lọc theo chủ đề và tìm kiếm từ khóa.
  - Xử lý tương thích song ngữ các trường DTO/Database (`ma_tri_thuc`/`id`, `chu_de`/`topic`, `cau_hoi_mau`/`question`, `noi_dung`/`content`).
- [x] **Task 5.1.2: Các Endpoint CRUD Quản trị Tri thức (`src/router/chat_router.py`)**
  - `GET /api/chat/knowledge`: Lấy danh sách tri thức có hỗ trợ bộ lọc và phân trang.
  - `POST /api/chat/knowledge`: Thêm mới tri thức vào CSDL Supabase.
  - `PUT /api/chat/knowledge/{id}`: Cập nhật nội dung câu hỏi mẫu và câu trả lời.
  - `DELETE /api/chat/knowledge/{id}`: Xóa tri thức khỏi kho dữ liệu tuyển sinh.

---

### TASK 2 (SPRINT 5): ĐỒNG BỘ TỨC THÌ BỘ NHỚ RAM RAG BM25 (DYNAMIC RE-INDEXING)
> **Mục tiêu**: Ngăn chặn rủi ro "Giao diện hoặc CSDL đã đổi nhưng Chatbot vẫn trả lời nội dung cũ".
- [x] **Task 5.2.1: Cơ chế Tự động Kích hoạt `sync_knowledge()` sau mỗi thao tác Ghi**
  - Khi có sự kiện `POST/PUT/DELETE` tri thức thành công, hệ thống tự động rebuild lại chỉ mục BM25 trong bộ nhớ RAM on-the-fly mà không cần restart server.
- [x] **Task 5.2.2: Endpoint Đồng bộ Thủ công (`POST /api/chat/sync-knowledge`)**
  - Cung cấp API cho phép Admin hoặc Cron job chủ động kích hoạt quét lại toàn bộ CSDL và đồng bộ RAM RAG.

---

### TASK 3 (SPRINT 5): BẢO MẬT & PHÂN QUYỀN KHO TRI THỨC ADMIN
> **Mục tiêu**: Ngăn chặn người dùng thiếu quyền chỉnh sửa dữ liệu tri thức của nhà trường.
- [x] **Task 5.3.1: Cơ chế Xác thực Khóa Quản trị (`src/core/security.py`)**
  - Tích hợp dependency `verify_internal_api_key` kiểm tra Header `X-Internal-API-Key` hoặc `Authorization Bearer`.
  - Từ chối ngay lập tức (HTTP 401 Unauthorized) các yêu cầu không có quyền hợp lệ.

---

### TASK 4 (SPRINT 5): BẢO VỆ RANH GIỚI NGHIỆP VỤ: TÁCH BIỆT DỰ BÁO AI KHỎI KẾT QUẢ TRÚNG TUYỂN
> **Mục tiêu**: Đảm bảo dự báo AI tuyệt đối không can thiệp hay gây hiểu nhầm là kết quả trúng tuyển chính thức.
- [x] **Task 5.4.1: Nhãn Dữ liệu Minh bạch trong API Đánh giá Điểm (`src/schemas/prediction_schema.py`)**
  - Toàn bộ kết quả từ `POST /api/predict/admission-chance` và `POST /api/predict/recommend-majors` chỉ trả về:
    - `xac_suat_trung_tuyen` (0–100%)
    - `muc_do_an_toan` (An toàn, Thử thách, Rủi ro)
    - `nhan_xet_chuyen_gia` (Mang tính tư vấn định hướng)
  - Tuyệt đối không trả về cờ "Đã trúng tuyển" hoặc quyết định xét tuyển chính thức.

---

# =====================================================================
# SPRINT 6: ĐÓNG BĂNG MÃ NGUỒN AI, KIỂM THỬ HỒI QUY XUYÊN LUỒNG & BACKLOG MÔ HÌNH [HOÀN THÀNH 100%]
# =====================================================================
> **Đối chiếu SPRINT-6.md**: Đóng băng logic lõi AI/ML theo đúng phạm vi phân công ("Không bổ sung hoặc sửa source backend AI"), bảo vệ tính toàn vẹn hệ thống và giữ vững hồi quy khi các service khác chốt điểm và công bố kết quả.

### TASK 1 (SPRINT 6): ĐÓNG BĂNG MÃ NGUỒN LÕI BACKEND AI (FROZEN CORE AI)
> **Mục tiêu**: Tuân thủ nguyên tắc "Không bổ sung hoặc sửa source backend AI" trong Sprint 6; bảo toàn độ ổn định của MBTI, Chatbot và Predictor.
- [x] **Task 6.1.1: Khóa Ranh giới Dữ liệu Điểm chuẩn Chính thức**
  - Bảng quy đổi điểm và công thức của AI chỉ phục vụ mục đích dự báo và tư vấn thí sinh.
  - Backend Điểm và Next.js chịu trách nhiệm hoàn toàn về quy tắc chốt điểm thực tế và công bố danh sách trúng tuyển.

---

### TASK 2 (SPRINT 6): DUY TRÌ BỘ KIỂM THỬ HỒI QUY TOÀN DIỆN (FULL REGRESSION TEST SUITE)
> **Mục tiêu**: Đảm bảo 100% test case xanh khi các service liên quan tiến hành tích hợp và nghiệm thu.
- [x] **Task 6.2.1: Bộ Kiểm thử Tự động 226/226 Test Cases Pass 100%**
  - Duy trì kiểm thử hồi quy 16 nhóm tính cách MBTI, xử lý chuỗi câu trả lời, RAG fallback, phân quyền tri thức và tính điểm ưu tiên giảm trừ tuyến tính.
- [x] **Task 6.2.2: Tích hợp Toàn diện `HeadMethodMiddleware` Phục vụ Giám sát Uptime 24/7**
  - Hỗ trợ phương thức `HEAD` trên toàn bộ endpoint GET (bao gồm `/health`, `/api/health`, `/api/mbti/questions`, `/api/predict/*`) giúp UptimeRobot giám sát 24/7 không bị lỗi 405.

---

### TASK 3 (SPRINT 6): LỚP TƯƠNG THÍCH HAI CHIỀU CHO FRONTEND NEXT.JS (BIDIRECTIONAL COMPATIBILITY)
> **Mục tiêu**: Đảm bảo Frontend Next.js gọi trực tiếp vào backend AI không bị lỗi kiểu dữ liệu hoặc fallback sang client mock.
- [x] **Task 6.3.1: Tương thích Chatbot (`ChatResponseData.reply`)**
  - Bổ sung `@computed_field reply` đồng nhất với `answer`.
- [x] **Task 6.3.2: Tương thích Câu hỏi & Đáp án MBTI**
  - Tự động chuẩn hóa đáp án chữ cái `"A"` $	o 5$ và `"B"` $	o 1$; sinh các trường `question`, `option_a`, `option_b`, `scores`, `ma_chuong_trinh`, `ten_chuong_trinh`.
- [x] **Task 6.3.3: Tương thích Đánh giá Xác suất (`chance_percentage`, `evaluation`)**
  - Pre-validator tự động phân rã `diem_xet_tuyen` sang 3 môn tổ hợp, nhận diện cả mã ngành mới `GHAxx` lẫn mã cũ Bộ GD&ĐT `7xxxxxx`.

---

### TASK 4 (BACKLOG DÀI HẠN SAU SPRINT 6): HỆ THỐNG GHI NHẬN PHẢN HỒI & ĐÁNH GIÁ MÔ HÌNH
> **Mục tiêu**: Chuẩn bị kiến trúc cho giai đoạn vận hành thực tế sau khi công bố kết quả tuyển sinh.
- [ ] **Task 6.4.1: Thu thập Đánh giá Phản hồi Chatbot từ Thí sinh (Chatbot Feedback Logging)**
  - Lưu trữ đánh giá Hài lòng / Không hài lòng (Upvote / Downvote) kèm lý do góp ý từ thí sinh để đánh giá độ chính xác của câu trả lời.
- [ ] **Task 6.4.2: Đánh giá Độ lệch Mô hình sau Mùa Tuyển sinh (Post-Admission Model Calibration)**
  - Tự động so sánh điểm chuẩn thực tế được Hội đồng công bố với điểm dự báo của Huber Regressor để tính toán sai số $MAE$, $RMSE$ và tái huấn luyện mô hình cho mùa tuyển sinh tiếp theo.
