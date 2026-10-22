# TÀI LIỆU CẤU TRÚC CƠ SỞ DỮ LIỆU SUPABASE (DATABASE_SCHEMA.md)

> **Dự án**: Tuyển sinh Đại học Giao thông Vận tải (UTC) - Microservice AI/ML
> **Tổng số bảng (public schema)**: 26
> **Thời gian trích xuất**: 2026-10-03

---

## 📌 BẢNG TỔNG QUAN CÁC BẢNG

| TT | Tên bảng | Số dòng dữ liệu | Vai trò chính |
| :-: | :--- | :-: | :--- |
| 1 | `_prisma_migrations` | **5** | Dữ liệu hệ thống |
| 2 | `admin` | **1** | Tài khoản cán bộ quản trị hệ thống |
| 3 | `bang_diem` | **0** | Dữ liệu hệ thống |
| 4 | `chung_chi` | **0** | Dữ liệu hệ thống |
| 5 | `chuong_trinh_dao_tao` | **109** | Khung chương trình đào tạo chi tiết |
| 6 | `ctdt_hoc_phan` | **0** | Dữ liệu hệ thống |
| 7 | `ctdt_to_hop` | **0** | Dữ liệu hệ thống |
| 8 | `danh_muc_mon_hoc` | **0** | Dữ liệu hệ thống |
| 9 | `diem_chi_tiet` | **0** | Dữ liệu hệ thống |
| 10 | `diem_to_hop` | **0** | Dữ liệu hệ thống |
| 11 | `diem_trung_tuyen` | **533** | Điểm chuẩn theo phương thức & tiêu chí phụ |
| 12 | `du_doan_diem_chuan` | **0** | Lưu nhật ký chạy mô hình dự báo điểm chuẩn |
| 13 | `giai_thuong` | **0** | Dữ liệu hệ thống |
| 14 | `hoc_phan` | **0** | Dữ liệu hệ thống |
| 15 | `ket_qua_trac_nghiem` | **0** | Lưu kết quả trắc nghiệm tính cách MBTI |
| 16 | `khoi_nganh` | **4** | Khối ngành (Kỹ thuật, Kinh tế, Ngoại ngữ...) |
| 17 | `lich_su_diem_chuan` | **253** | Điểm chuẩn & chỉ tiêu lịch sử các năm (2021-2025) |
| 18 | `lo_trinh_tuyen_sinh` | **0** | Các mốc thời gian tuyển sinh quan trọng |
| 19 | `nganh_hoc` | **69** | Danh mục 69 ngành đào tạo UTC |
| 20 | `nguyen_vong_sinh_vien` | **0** | Nguyện vọng đăng ký của thí sinh |
| 21 | `phuong_thuc_xet_tuyen` | **5** | Các phương thức tuyển sinh (PT1, PT2, PT3, PT4...) |
| 22 | `thi_sinh` | **0** | Thông tin thí sinh đăng ký tư vấn |
| 23 | `to_hop_xet_tuyen` | **0** | Danh mục tổ hợp môn xét tuyển (A00, A01, D01...) |
| 24 | `trang_noi_dung` | **0** | Tin tức & bài viết đề án tuyển sinh |
| 25 | `tri_thuc_ai` | **132** | Kho tri thức tuyển sinh cho Chatbot RAG |
| 26 | `cau_hoi_mbti` | **20** | Ngân hàng 20 câu hỏi trắc nghiệm MBTI hướng nghiệp UTC |

---

## 📋 CHI TIẾT CẤU TRÚC VÀ CỘT DỮ LIỆU TỪNG BẢNG

### 1. Bảng `_prisma_migrations`

- **Số lượng bản ghi**: 5

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `id` | `character varying` | NO | None |
| `checksum` | `character varying` | NO | None |
| `finished_at` | `timestamp with time zone` | YES | None |
| `migration_name` | `character varying` | NO | None |
| `logs` | `text` | YES | None |
| `rolled_back_at` | `timestamp with time zone` | YES | None |
| `started_at` | `timestamp with time zone` | NO | `now()` |
| `applied_steps_count` | `integer` | NO | `0` |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "id": "1ee4629a-9ac1-4fce-8cf7-c9aa6d34616f",
    "checksum": "293ef7cccecf3c248b3a422bf4adbe130869fb4151d28844fe1acb6a00cd2abd",
    "finished_at": "2026-09-21T16:39:21.815025+00:00",
    "migration_name": "20260921163917_init",
    "logs": null,
    "rolled_back_at": null,
    "started_at": "2026-09-21T16:39:17.793451+00:00",
    "applied_steps_count": 1
  },
  {
    "id": "d3c0c050-0c4e-4ec8-8a98-5212b94cce0d",
    "checksum": "04813dea3fe35e915f9f2d0672533d40e0fe145b095db03536e7647dbf6f0b93",
    "finished_at": "2026-09-21T16:49:22.631502+00:00",
    "migration_name": "20260921164921_insert_hoc_phan",
    "logs": null,
    "rolled_back_at": null,
    "started_at": "2026-09-21T16:49:22.027039+00:00",
    "applied_steps_count": 1
  }
]
```

### 2. Bảng `admin`

- **Số lượng bản ghi**: 1

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_admin` | `text` | NO | None |
| `ho_ten` | `text` | NO | None |
| `email` | `text` | NO | None |
| `mat_khau` | `text` | NO | None |
| `vai_tro` | `USER-DEFINED` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_admin": "00000000-0000-0000-0000-000000000000",
    "ho_ten": "System Seed",
    "email": "seed@utc.edu.vn",
    "mat_khau": "CHANGE_ME_HASH",
    "vai_tro": "super_admin",
    "create_at": "2026-09-27T14:58:58.121000"
  }
]
```

### 3. Bảng `bang_diem`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_bang_diem` | `text` | NO | None |
| `cccd` | `character varying` | NO | None |
| `loai_diem` | `USER-DEFINED` | NO | None |
| `nam_hoc` | `integer` | NO | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 4. Bảng `chung_chi`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_chung_chi` | `text` | NO | None |
| `cccd` | `character varying` | NO | None |
| `loai_chung_chi` | `text` | NO | None |
| `diem_hoac_hang` | `text` | NO | None |
| `ngay_cap` | `date` | YES | None |
| `ngay_het_han` | `date` | YES | None |
| `file_dinh_kem` | `text` | NO | None |
| `trang_thai_duyet` | `USER-DEFINED` | NO | `'cho'::trang_thai_duyet` |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 5. Bảng `chuong_trinh_dao_tao`

- **Số lượng bản ghi**: 109

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_chuong_trinh` | `text` | NO | None |
| `ma_nganh` | `text` | NO | None |
| `ten_chuong_trinh` | `text` | NO | None |
| `de_cuong` | `text` | YES | None |
| `chuan_dau_ra` | `text` | YES | None |
| `ma_admin_quan_ly` | `text` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_chuong_trinh": "7310101",
    "ma_nganh": "7310101",
    "ten_chuong_trinh": "Kinh tế",
    "de_cuong": null,
    "chuan_dau_ra": null,
    "ma_admin_quan_ly": "00000000-0000-0000-0000-000000000000",
    "create_at": "2026-09-27T14:58:58.121000"
  },
  {
    "ma_chuong_trinh": "7340101",
    "ma_nganh": "7340101",
    "ten_chuong_trinh": "Quản trị kinh doanh",
    "de_cuong": null,
    "chuan_dau_ra": null,
    "ma_admin_quan_ly": "00000000-0000-0000-0000-000000000000",
    "create_at": "2026-09-27T14:58:58.121000"
  }
]
```

### 6. Bảng `ctdt_hoc_phan`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_ctdt_hoc_phan` | `text` | NO | None |
| `ma_chuong_trinh` | `text` | NO | None |
| `ma_hoc_phan` | `text` | NO | None |
| `nam_ap_dung` | `integer` | NO | None |
| `hoc_ky` | `integer` | NO | None |
| `loai` | `USER-DEFINED` | NO | `'bat_buoc'::loai_hoc_phan` |
| `khoi_kien_thuc` | `text` | YES | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 7. Bảng `ctdt_to_hop`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_ctdt_to_hop` | `text` | NO | None |
| `ma_chuong_trinh` | `text` | NO | None |
| `ma_to_hop` | `text` | NO | None |
| `nam` | `integer` | NO | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 8. Bảng `danh_muc_mon_hoc`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_mon` | `text` | NO | None |
| `ten_mon` | `text` | NO | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 9. Bảng `diem_chi_tiet`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_chi_tiet` | `text` | NO | None |
| `ma_bang_diem` | `text` | NO | None |
| `ma_mon` | `text` | NO | None |
| `diem_so` | `double precision` | YES | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 10. Bảng `diem_to_hop`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_diem_to_hop` | `text` | NO | None |
| `cccd` | `character varying` | NO | None |
| `ma_bang_diem` | `text` | NO | None |
| `ma_to_hop` | `text` | NO | None |
| `tong_diem_goc` | `double precision` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 11. Bảng `diem_trung_tuyen`

- **Số lượng bản ghi**: 533

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_diem_tt` | `text` | NO | None |
| `ma_ls_dc` | `text` | NO | None |
| `ma_phuong_thuc` | `text` | NO | None |
| `diem` | `double precision` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |
| `diem_uu_tien_toi_thieu` | `double precision` | YES | None |
| `dieu_kien_mon` | `jsonb` | YES | None |
| `nguyen_vong_toi_da` | `integer` | YES | None |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_diem_tt": "a03e2ec5-aa40-5847-8f8d-c049fc59c408",
    "ma_ls_dc": "ad54ee37-6a9e-5a8a-acc5-739e12612c87",
    "ma_phuong_thuc": "PT1",
    "diem": 25.15,
    "create_at": "2026-09-27T14:58:58.121000",
    "diem_uu_tien_toi_thieu": null,
    "dieu_kien_mon": [
      {
        "mon": "toan",
        "diem_toi_thieu": 7.4
      }
    ],
    "nguyen_vong_toi_da": 2
  },
  {
    "ma_diem_tt": "df11b3fd-098b-561a-b966-48ff2a966069",
    "ma_ls_dc": "94d3db96-67ba-5330-9fd4-3785f25a20ab",
    "ma_phuong_thuc": "PT1",
    "diem": 25.3,
    "create_at": "2026-09-27T14:58:58.121000",
    "diem_uu_tien_toi_thieu": null,
    "dieu_kien_mon": [
      {
        "mon": "toan",
        "diem_toi_thieu": 7.8
      }
    ],
    "nguyen_vong_toi_da": 3
  }
]
```

### 12. Bảng `du_doan_diem_chuan`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_du_doan_dc` | `text` | NO | None |
| `ma_chuong_trinh` | `text` | NO | None |
| `nam_du_doan` | `integer` | NO | None |
| `diem_du_doan` | `double precision` | NO | None |
| `ngay_tinh_toan` | `timestamp without time zone` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 13. Bảng `giai_thuong`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_giai_thuong` | `text` | NO | None |
| `cccd` | `character varying` | NO | None |
| `giai_thuong` | `USER-DEFINED` | NO | None |
| `loai_giai_thuong` | `USER-DEFINED` | NO | None |
| `mon_hoc` | `USER-DEFINED` | NO | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 14. Bảng `hoc_phan`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_hoc_phan` | `text` | NO | None |
| `ten_hoc_phan` | `text` | NO | None |
| `so_tin_chi` | `integer` | NO | None |
| `so_tiet_ly_thuyet` | `integer` | YES | `0` |
| `so_tiet_thuc_hanh` | `integer` | YES | `0` |
| `mo_ta` | `text` | YES | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 15. Bảng `ket_qua_trac_nghiem`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_ket_qua` | `text` | NO | None |
| `cccd` | `character varying` | YES | None |
| `session_id` | `text` | NO | None |
| `nhom_tinh_cach` | `text` | YES | None |
| `goi_y_nganh` | `text` | YES | None |
| `thoi_gian_thuc_hien` | `timestamp without time zone` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 16. Bảng `khoi_nganh`

- **Số lượng bản ghi**: 4

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_khoi_nganh` | `text` | NO | None |
| `ten_khoi_nganh` | `text` | NO | None |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_khoi_nganh": "KHOI_CN",
    "ten_khoi_nganh": "Khối Công nghệ & CNTT"
  },
  {
    "ma_khoi_nganh": "KHOI_KT",
    "ten_khoi_nganh": "Khối Kinh tế & Vận tải"
  }
]
```

### 17. Bảng `lich_su_diem_chuan`

- **Số lượng bản ghi**: 253

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_ls_dc` | `text` | NO | None |
| `ma_chuong_trinh` | `text` | NO | None |
| `nam` | `integer` | NO | None |
| `chi_tieu` | `integer` | NO | None |
| `trung_tuyen` | `integer` | YES | None |
| `ma_admin_cap_nhat` | `text` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_ls_dc": "ad54ee37-6a9e-5a8a-acc5-739e12612c87",
    "ma_chuong_trinh": "7310101",
    "nam": 2021,
    "chi_tieu": 80,
    "trung_tuyen": 80,
    "ma_admin_cap_nhat": "00000000-0000-0000-0000-000000000000",
    "create_at": "2026-09-27T14:58:58.121000"
  },
  {
    "ma_ls_dc": "94d3db96-67ba-5330-9fd4-3785f25a20ab",
    "ma_chuong_trinh": "7340101",
    "nam": 2021,
    "chi_tieu": 110,
    "trung_tuyen": 110,
    "ma_admin_cap_nhat": "00000000-0000-0000-0000-000000000000",
    "create_at": "2026-09-27T14:58:58.121000"
  }
]
```

### 18. Bảng `lo_trinh_tuyen_sinh`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_su_kien` | `text` | NO | None |
| `ten_su_kien` | `text` | NO | None |
| `thoi_gian_bat_dau` | `timestamp without time zone` | NO | None |
| `thoi_gian_ket_thuc` | `timestamp without time zone` | YES | None |
| `ghi_chu` | `text` | YES | None |
| `ma_admin_cap_nhat` | `text` | NO | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 19. Bảng `nganh_hoc`

- **Số lượng bản ghi**: 69

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_nganh` | `text` | NO | None |
| `ten_nganh` | `text` | NO | None |
| `khoi_kien_thuc` | `text` | YES | None |
| `ma_admin_quan_ly` | `text` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |
| `ma_khoi_nganh` | `text` | YES | None |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_nganh": "7220201",
    "ten_nganh": "Ngôn ngữ Anh",
    "khoi_kien_thuc": null,
    "ma_admin_quan_ly": "00000000-0000-0000-0000-000000000000",
    "create_at": "2026-09-27T14:58:58.121000",
    "ma_khoi_nganh": "KHOI_NN"
  },
  {
    "ma_nganh": "7310101",
    "ten_nganh": "Kinh tế",
    "khoi_kien_thuc": null,
    "ma_admin_quan_ly": "00000000-0000-0000-0000-000000000000",
    "create_at": "2026-09-27T14:58:58.121000",
    "ma_khoi_nganh": "KHOI_KT"
  }
]
```

### 20. Bảng `nguyen_vong_sinh_vien`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_ho_so` | `text` | NO | None |
| `cccd` | `character varying` | NO | None |
| `ma_chuong_trinh` | `text` | NO | None |
| `trang_thai` | `USER-DEFINED` | NO | `'cho'::trang_thai_duyet` |
| `ket_qua` | `text` | YES | None |
| `diem_uu_tien_ap_dung` | `double precision` | YES | None |
| `tong_diem_xet_tuyen` | `double precision` | YES | None |
| `ma_to_hop` | `text` | YES | None |
| `ma_phuong_thuc` | `text` | NO | None |
| `nguon_du_lieu` | `USER-DEFINED` | NO | None |
| `nguyen_vong` | `integer` | NO | None |
| `nam_tuyen_sinh` | `integer` | NO | None |
| `ma_admin_xu_ly` | `text` | YES | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 21. Bảng `phuong_thuc_xet_tuyen`

- **Số lượng bản ghi**: 5

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_phuong_thuc` | `text` | NO | None |
| `ten_phuong_thuc` | `text` | NO | None |

**Dữ liệu mẫu tiêu biểu:**

```json
[
  {
    "ma_phuong_thuc": "PT1",
    "ten_phuong_thuc": "Điểm thi thpt"
  },
  {
    "ma_phuong_thuc": "PT2",
    "ten_phuong_thuc": "Học bạ"
  }
]
```

### 22. Bảng `thi_sinh`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `cccd` | `character varying` | NO | None |
| `ho_ten` | `text` | NO | None |
| `so_dien_thoai` | `text` | NO | None |
| `khu_vuc` | `text` | YES | None |
| `doi_tuong_uu_tien` | `text` | YES | None |
| `diem_uu_tien_he_thong` | `double precision` | YES | `0` |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 23. Bảng `to_hop_xet_tuyen`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_to_hop` | `text` | NO | None |
| `ma_mon_1` | `text` | NO | None |
| `ma_mon_2` | `text` | NO | None |
| `ma_mon_3` | `text` | NO | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 24. Bảng `trang_noi_dung`

- **Số lượng bản ghi**: 0

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_bai_viet` | `text` | NO | None |
| `tieu_de` | `text` | NO | None |
| `noi_dung_html` | `text` | NO | None |
| `chuyen_muc` | `text` | NO | None |
| `ma_admin_tac_gia` | `text` | NO | None |
| `ngay_dang` | `timestamp without time zone` | YES | None |

*(Bảng hiện chưa có bản ghi dữ liệu)*

### 25. Bảng `tri_thuc_ai`

- **Số lượng bản ghi**: 132

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `ma_tri_thuc` | `text` | NO | None |
| `chu_de` | `text` | NO | None |
| `cau_hoi_mau` | `text` | YES | None |
| `noi_dung` | `text` | NO | None |
| `trang_thai` | `text` | NO | `'active'::text` |
| `ma_admin_phu_trach` | `text` | NO | None |
| `create_at` | `timestamp without time zone` | NO | `CURRENT_TIMESTAMP` |

### 26. Bảng `cau_hoi_mbti`

- **Số lượng bản ghi**: 20

| Cột (Field) | Kiểu dữ liệu (Data Type) | Cho phép Null | Giá trị mặc định |
| :--- | :--- | :-: | :--- |
| `id` | `integer` | NO | `nextval('cau_hoi_mbti_id_seq'::regclass)` |
| `noi_dung` | `text` | NO | None |
| `chieu_do` | `character varying(10)` | NO | None |
| `chieu_tich_cuc` | `character varying(5)` | NO | None |
| `linh_vuc_ngu_canh` | `character varying(255)` | YES | None |
| `trang_thai` | `character varying(20)` | YES | `'active'::character varying` |
| `create_at` | `timestamp with time zone` | YES | `CURRENT_TIMESTAMP` |

