import math
from typing import Any, Dict, List, Optional
from src.core.exceptions import NotFoundException
from src.ml.news.news_engine import news_engine
from src.ml.prediction.admission_predictor import admission_predictor
from src.ml.prediction.benchmark_predictor import benchmark_predictor
from src.ml.prediction.cold_start_engine import cold_start_engine
from src.ml.prediction.dynamic_predictor import dynamic_predictor
from src.repositories.prediction_repository import prediction_repository
from src.schemas.prediction_schema import (
    AdmissionChanceRequest,
    BenchmarkPredictionItem,
    BenchmarkScenarioRequest,
    ColdStartMajorDetail,
    ColdStartMajorRequest,
    ColdStartNeighbor,
    DynamicBenchmarkDetail,
    DynamicTimelinePoint,
    EquivalentMethodScores,
    MajorChanceResult,
    MajorRecommendationData,
    NewsArticleItem,
    PercentileEquatingDetail,
    PercentileEquatingRequest,
    StrategyTier,
)


class PredictionService:
    def __init__(self):
        self.repo = prediction_repository
        self.predictor = benchmark_predictor
        self.evaluator = admission_predictor
        self.dynamic_predictor = dynamic_predictor
        self.news_engine = news_engine
        self.cold_start_engine = cold_start_engine

    def calibrate_major_cutoff(
        self,
        ma_chuong_trinh: str,
        base_cutoff: float,
        quota_change_percent: float = 0.0,
        macro_exam_delta: float = 0.0,
    ) -> float:
        quota_effect = -0.15 * (quota_change_percent / 10.0)
        calibrated = base_cutoff + macro_exam_delta + quota_effect
        return round(float(min(29.5, max(14.0, calibrated))), 2)

    def build_item(self, row: dict) -> BenchmarkPredictionItem:
        code = row["ma_chuong_trinh"]
        raw_pred = round(float(row["diem_du_doan"]), 2)
        pred_score = self.calibrate_major_cutoff(code, raw_pred)
        base_score = round(float(row["diem_chuan_2025"]), 2)
        delta = round(pred_score - base_score, 2)

        methods_dict = self.predictor.convert_thpt_to_all_methods(pred_score)
        equiv_scores = EquivalentMethodScores(
            pt1_thpt=methods_dict["pt1_thpt"],
            pt2_hoc_ba=methods_dict["pt2_hoc_ba"],
            pt3_hsa=methods_dict["pt3_hsa"],
            pt4_tsa=methods_dict["pt4_tsa"],
        )

        trend = self.predictor.determine_trend(delta)
        factors = self.predictor.get_influencing_factors(code, delta)
        combos = (
            self.predictor.anchors.get(code, {}).get("to_hop_xet_tuyen") or ["A00"]
        )

        return BenchmarkPredictionItem(
            ma_chuong_trinh=code,
            ten_chuong_trinh=row["ten_chuong_trinh"],
            chi_tieu_2025=row.get("chi_tieu_2025"),
            chi_tieu_2026=row.get("chi_tieu_2026"),
            diem_chuan_2025=base_score,
            diem_du_doan_2026=pred_score,
            score_range_min=round(pred_score - 0.35, 2),
            score_range_max=round(pred_score + 0.35, 2),
            trend=trend,
            delta_score=delta,
            phuong_thuc_quy_doi=equiv_scores,
            to_hop_xet_tuyen=combos,
            influencing_factors=factors,
        )

    def get_all_predictions(self) -> List[BenchmarkPredictionItem]:
        rows = self.repo.get_all_2026_predictions()
        return [self.build_item(r) for r in rows]

    def get_prediction_by_major(
        self, ma_chuong_trinh: str
    ) -> BenchmarkPredictionItem:
        row = self.repo.get_2026_prediction_by_major(ma_chuong_trinh)
        if not row:
            raise NotFoundException(
                f"Không tìm thấy chương trình đào tạo mã: {ma_chuong_trinh}"
            )
        return self.build_item(row)

    def simulate_scenario(
        self, request: BenchmarkScenarioRequest
    ) -> BenchmarkPredictionItem:
        code = request.ma_chuong_trinh
        row = self.repo.get_2026_prediction_by_major(code)
        if not row:
            raise NotFoundException(
                f"Không tìm thấy chương trình đào tạo mã: {code}"
            )

        sim_score = self.predictor.predict_scenario(
            ma_chuong_trinh=code,
            custom_quota_growth=request.custom_quota_growth,
            custom_macro_delta=request.custom_macro_delta,
        )

        sim_row = {
            "ma_chuong_trinh": code,
            "ten_chuong_trinh": row["ten_chuong_trinh"],
            "diem_du_doan": sim_score,
            "chi_tieu_2025": row.get("chi_tieu_2025"),
            "chi_tieu_2026": row.get("chi_tieu_2026"),
            "diem_chuan_2025": row.get("diem_chuan_2025"),
        }
        return self.build_item(sim_row)

    def map_major_to_sector(
        self, ma_chuong_trinh: str, ten_chuong_trinh: str = ""
    ) -> str:
        clean_name = ten_chuong_trinh.lower()
        clean_code = ma_chuong_trinh.lower()

        if any(k in clean_name for k in ["tiếng anh", "ngôn ngữ anh"]):
            return "ENGLISH"
        if any(k in clean_name for k in ["bán dẫn", "vi mạch"]) or clean_code == "gha33":
            return "SEMICONDUCTOR"
        if any(k in clean_name for k in ["đường sắt", "metro"]) or "ds" in clean_code:
            return "RAILWAY"
        if any(
            k in clean_name
            for k in [
                "công nghệ thông tin",
                "khoa học máy tính",
                "toán tin",
                "phần mềm",
                "trí tuệ nhân tạo",
                "máy tính",
            ]
        ) or clean_code in ["gha13", "gha14", "gha14qt"]:
            return "IT_CS"
        if any(k in clean_name for k in ["logistics", "chuỗi cung ứng"]) or clean_code in ["gha10", "gha10qt"]:
            return "LOGISTICS"
        if any(
            k in clean_name
            for k in [
                "xây dựng",
                "cầu đường",
                "cầu và kết cấu",
                "công trình",
                "thủy",
                "địa kỹ thuật",
                "hạ tầng",
            ]
        ) or clean_code in ["gha28", "gha31", "gha32"]:
            return "CIVIL_CONSTRUCTION"
        if any(
            k in clean_name
            for k in [
                "kinh tế",
                "quản trị",
                "tài chính",
                "ngân hàng",
                "kế toán",
                "vận tải",
                "du lịch",
                "thương mại",
            ]
        ):
            return "ECONOMICS"
        return "GENERAL"

    def get_curated_market_news(
        self, sector: Optional[str] = None
    ) -> List[Dict[str, Any]]:
        articles = [
            {
                "title": "Tác động của Generative AI và sự tái cấu trúc nguồn nhân lực công nghệ thông tin",
                "link": "https://vietnamnet.vn/nhan-luc-cntt-va-lan-song-ai-2026",
                "published_date": "2026-10-15",
                "source": "VietnamNet",
                "sector": "IT_CS",
                "sentiment_score": -0.35,
                "summary": "Doanh nghiệp công nghệ dịch chuyển tuyển dụng sang nhân sự AI cấp cao, nhu cầu lập trình viên sơ cấp giảm nhẹ.",
            },
            {
                "title": "Chính phủ phê duyệt siêu dự án Đường sắt tốc độ cao Bắc - Nam 67 tỷ USD, khát hàng chục ngàn kỹ sư",
                "link": "https://vnexpress.net/khoi-cong-duong-sat-toc-do-cao-khat-ky-su",
                "published_date": "2026-10-18",
                "source": "VnExpress",
                "sector": "RAILWAY",
                "sentiment_score": 0.85,
                "summary": "Nhu cầu đào tạo kỹ sư đường sắt tốc độ cao, kỹ thuật metro tại UTC tăng vọt với hàng loạt chính sách học bổng và cam kết tuyển dụng.",
            },
            {
                "title": "Đầu tư hạ tầng giao thông và cao tốc Bắc Nam thúc đẩy nhu cầu kỹ sư Cầu đường",
                "link": "https://dantri.com.vn/giao-thong-ha-tang-nhan-luc",
                "published_date": "2026-10-12",
                "source": "Dân Trí",
                "sector": "CIVIL_CONSTRUCTION",
                "sentiment_score": 0.60,
                "summary": "Hàng loạt đại dự án sân bay Long Thành và mạng lưới cao tốc kéo theo sức cầu lớn về kỹ sư xây dựng công trình giao thông.",
            },
            {
                "title": "Chiến lược quốc gia phát triển công nghiệp bán dẫn đến năm 2030, tầm nhìn 2050",
                "link": "https://chinhphu.vn/chien-luoc-vi-mach-ban-dan",
                "published_date": "2026-10-10",
                "source": "Cổng TTĐT Chính Phủ",
                "sector": "SEMICONDUCTOR",
                "sentiment_score": 0.90,
                "summary": "Mục tiêu đào tạo 50.000 kỹ sư vi mạch bán dẫn mở ra cơ hội đột phá cho ngành kỹ thuật điện tử bán dẫn.",
            },
            {
                "title": "Logistics và chuỗi cung ứng giữ vững đà tăng trưởng cùng xuất nhập khẩu",
                "link": "https://tuoitre.vn/logistics-viet-nam-tang-truong",
                "published_date": "2026-10-14",
                "source": "Tuổi Trẻ",
                "sector": "LOGISTICS",
                "sentiment_score": 0.50,
                "summary": "Ngành logistics tiếp tục khẳng định vị thế trụ cột kinh tế với mức điểm chuẩn dự báo giữ đà tăng ổn định.",
            },
            {
                "title": "Thị trường tài chính ngân hàng duy trì nhu cầu tuyển dụng cử nhân kinh tế chất lượng cao",
                "link": "https://baodautu.vn/tai-chinh-ngan-hang-tuyen-dung",
                "published_date": "2026-10-08",
                "source": "Báo Đầu Tư",
                "sector": "ECONOMICS",
                "sentiment_score": 0.20,
                "summary": "Khối ngành kinh tế vận tải và tài chính tiếp tục thu hút lượng lớn nguyện vọng đăng ký xét tuyển.",
            },
            {
                "title": "Chứng chỉ tiếng Anh quốc tế tiếp tục là lợi thế xét tuyển vào các trường đại học tốp đầu",
                "link": "https://giaoduc.net.vn/loi-the-tieng-anh-tuyen-sinh",
                "published_date": "2026-10-16",
                "source": "Giáo dục Việt Nam",
                "sector": "ENGLISH",
                "sentiment_score": 0.40,
                "summary": "Xu hướng tuyển sinh kết hợp chứng chỉ IELTS/TOEFL giúp thí sinh gia tăng đáng kể cơ hội trúng tuyển sớm.",
            },
        ]
        if sector and sector != "ALL":
            filtered = [
                a
                for a in articles
                if a["sector"] == sector or a["sector"] == "GENERAL"
            ]
            return filtered if filtered else articles
        return articles

    def get_market_news(
        self, sector: Optional[str] = None
    ) -> List[NewsArticleItem]:
        raw_items = self.get_curated_market_news(sector)
        return [NewsArticleItem(**a) for a in raw_items]

    def generate_simulated_applications(
        self, prior_score: float, quota: int, total_days: int = 30
    ) -> List[Dict[str, Any]]:
        total_candidates = max(50, quota * 4)
        apps = []
        for i in range(total_candidates):
            day = 1 + int(
                round((total_days - 1) * (i / max(1, total_candidates - 1)))
            )
            nv = 1 if i % 3 == 0 else (2 if i % 3 == 1 else 3)
            rank = i / max(1, total_candidates - 1)
            offset = -0.55 + 2.0 * (rank - 0.5) + 0.3 * math.sin(i * 0.35)
            score = round(float(min(29.5, max(14.0, prior_score + offset))), 2)
            apps.append(
                {
                    "id": f"cand_{i+1}",
                    "tong_diem": score,
                    "nguyen_vong": nv,
                    "day_offset": day,
                }
            )
        return apps

    def get_dynamic_trends(
        self, ma_chuong_trinh: str, total_days: int = 30
    ) -> DynamicBenchmarkDetail:
        row = self.repo.get_2026_prediction_by_major(ma_chuong_trinh)
        if not row:
            if ma_chuong_trinh in self.predictor.anchors:
                anchor = self.predictor.anchors[ma_chuong_trinh]
                row = {
                    "ma_chuong_trinh": ma_chuong_trinh,
                    "ten_chuong_trinh": anchor.get("ten_chuong_trinh", ma_chuong_trinh),
                    "diem_du_doan": anchor.get("diem_chuan_2025", 24.0),
                    "chi_tieu_2026": anchor.get("chi_tieu_2025", 100),
                }
            else:
                raise NotFoundException(
                    f"Không tìm thấy chương trình đào tạo mã: {ma_chuong_trinh}"
                )

        major_name = row.get("ten_chuong_trinh", ma_chuong_trinh)
        raw_cutoff = float(row.get("diem_du_doan", 24.0))
        prior_cutoff = self.calibrate_major_cutoff(ma_chuong_trinh, raw_cutoff)
        quota = int(row.get("chi_tieu_2026") or row.get("chi_tieu_2025") or 100)
        sector = self.map_major_to_sector(ma_chuong_trinh, major_name)

        articles = self.get_curated_market_news(sector)
        delta_news, relevant_articles = self.news_engine.compute_sector_trend_delta(
            articles, sector
        )

        sim_apps = self.generate_simulated_applications(
            prior_cutoff, quota, total_days
        )
        raw_timeline = self.dynamic_predictor.build_trend_timeline(
            prior_cutoff=prior_cutoff,
            historical_applications=sim_apps,
            quota=quota,
            total_days=total_days,
            news_delta=delta_news,
        )
        timeline = [DynamicTimelinePoint(**pt) for pt in raw_timeline]
        current_cutoff = (
            timeline[-1].predicted_cutoff if timeline else prior_cutoff
        )
        last_empirical = (
            timeline[-1].empirical_cutoff if timeline else prior_cutoff
        )

        if delta_news < -0.05 and current_cutoff > prior_cutoff:
            analysis_summary = (
                f"Chương trình '{major_name}' ({ma_chuong_trinh}) thuộc nhóm ngành {sector}. "
                f"Mặc dù mặt bằng điểm thí sinh nộp hồ sơ thực tế có xu hướng đẩy ngưỡng cắt lên {last_empirical:.2f} điểm, "
                f"nhưng tác động tiêu cực từ xu hướng thị trường (chỉ số delta: {delta_news}) đã kìm hãm bớt đà tăng, "
                f"đưa điểm chuẩn dự báo chốt ở mức {current_cutoff} điểm sau {total_days} ngày theo dõi liên tục."
            )
        elif delta_news < -0.05 and current_cutoff <= prior_cutoff:
            analysis_summary = (
                f"Chương trình '{major_name}' ({ma_chuong_trinh}) thuộc nhóm ngành {sector}. "
                f"Do tác động từ xu hướng thị trường thu hẹp tuyển dụng (chỉ số delta: {delta_news}) cùng phổ điểm thực tế, "
                f"điểm chuẩn dự báo đã hạ nhiệt từ {prior_cutoff} xuống {current_cutoff} điểm sau {total_days} ngày theo dõi."
            )
        elif delta_news > 0.05 and current_cutoff >= prior_cutoff:
            analysis_summary = (
                f"Chương trình '{major_name}' ({ma_chuong_trinh}) thuộc nhóm ngành {sector}. "
                f"Sức hút gia tăng từ thị trường việc làm (chỉ số delta: +{delta_news}) cộng hưởng cùng lượng hồ sơ nộp đông đảo "
                f"đã thúc đẩy điểm chuẩn tăng từ {prior_cutoff} lên {current_cutoff} điểm sau {total_days} ngày."
            )
        elif delta_news > 0.05 and current_cutoff < prior_cutoff:
            analysis_summary = (
                f"Chương trình '{major_name}' ({ma_chuong_trinh}) thuộc nhóm ngành {sector}. "
                f"Mặc dù thị trường có tín hiệu tích cực (chỉ số delta: +{delta_news}), phổ điểm thí sinh nộp thực tế "
                f"đã kéo điểm chuẩn điều chỉnh từ {prior_cutoff} về {current_cutoff} điểm sau {total_days} ngày."
            )
        else:
            analysis_summary = (
                f"Chương trình '{major_name}' ({ma_chuong_trinh}) duy trì ổn định quanh ngưỡng {current_cutoff} điểm. "
                f"Tốc độ nộp hồ sơ bám sát đường cong dự báo chuẩn."
            )

        news_insights = [NewsArticleItem(**a) for a in relevant_articles]

        return DynamicBenchmarkDetail(
            ma_chuong_trinh=ma_chuong_trinh,
            ten_chuong_trinh=major_name,
            chi_tieu=quota,
            prior_cutoff=prior_cutoff,
            current_cutoff=current_cutoff,
            news_impact_delta=delta_news,
            confidence_level="HIGH",
            timeline=timeline,
            news_insights=news_insights,
            analysis_summary=analysis_summary,
        )

    def evaluate_single_major_chance(
        self,
        code: str,
        norm_scores: dict,
        converted_en: float,
        region: Optional[str],
        group: Optional[str],
        major_data: Optional[dict] = None,
    ) -> MajorChanceResult:
        row = (
            major_data
            if major_data
            else self.repo.get_2026_prediction_by_major(code)
        )
        major_name = row["ten_chuong_trinh"] if row else code
        raw_cutoff = row["diem_du_doan"] if row else 24.0
        cutoff = self.calibrate_major_cutoff(code, float(raw_cutoff))

        allowed_combos = (
            self.predictor.anchors.get(code, {}).get("to_hop_xet_tuyen")
            or ["A00"]
        )
        best_combo, raw_score = self.evaluator.evaluate_best_combination(
            norm_scores, allowed_combos, converted_en
        )
        priority = self.evaluator.calculate_priority(raw_score, region, group)
        total_score = round(raw_score + priority, 2)

        gap, prob, level = self.evaluator.calculate_probability(
            total_score, cutoff
        )
        advice = self.evaluator.get_advice(level, gap, major_name)

        sector = self.map_major_to_sector(code, major_name)
        articles = self.get_curated_market_news(sector)
        news_delta, _ = self.news_engine.compute_sector_trend_delta(
            articles, sector
        )

        if news_delta < -0.15:
            trend_insight = (
                f"Xu hướng thị trường nhóm {sector} chịu tác động tái cấu trúc nhân lực "
                f"(delta: {news_delta}), điểm chuẩn có thể hạ nhẹ."
            )
        elif news_delta > 0.15:
            trend_insight = (
                f"Ngành {sector} đang đón đầu nhu cầu nhân lực và đầu tư phát triển "
                f"(delta: +{news_delta}), mức độ cạnh tranh dự kiến tăng."
            )
        else:
            trend_insight = (
                f"Điểm chuẩn ngành {major_name} duy trì ổn định, ít biến động đột biến."
            )

        return MajorChanceResult(
            ma_chuong_trinh=code,
            ten_chuong_trinh=major_name,
            diem_chuan_du_doan=round(cutoff, 2),
            to_hop_toi_uu=best_combo,
            diem_to_hop_goc=raw_score,
            diem_uu_tien=priority,
            tong_diem_xet_tuyen=total_score,
            do_lech_diem=gap,
            xac_suat_trung_tuyen=prob,
            muc_do_an_toan=level,
            nhan_xet_chuyen_gia=advice,
            confidence_level="HIGH",
            trend_insight=trend_insight,
        )

    def evaluate_admission_chance(
        self, request: AdmissionChanceRequest
    ) -> MajorChanceResult:
        norm_scores = self.evaluator.normalize_scores(request.academic_scores)
        converted_en = 0.0
        if request.foreign_language_cert:
            converted_en = self.evaluator.convert_english_certificate(
                request.foreign_language_cert.cert_type,
                request.foreign_language_cert.score,
            )

        target_code = request.target_major_code or "GHA14"
        row = self.repo.get_2026_prediction_by_major(target_code)
        if not row and target_code not in self.predictor.anchors:
            raise NotFoundException(
                f"Không tìm thấy chương trình đào tạo mã: {target_code}"
            )

        result = self.evaluate_single_major_chance(
            target_code,
            norm_scores,
            converted_en,
            request.priority_region,
            request.priority_group,
            major_data=row,
        )
        self.repo.record_evaluation(result.model_dump())
        return result

    def recommend_majors(
        self, request: AdmissionChanceRequest
    ) -> MajorRecommendationData:
        norm_scores = self.evaluator.normalize_scores(request.academic_scores)
        converted_en = 0.0
        if request.foreign_language_cert:
            converted_en = self.evaluator.convert_english_certificate(
                request.foreign_language_cert.cert_type,
                request.foreign_language_cert.score,
            )

        all_preds = self.repo.get_all_2026_predictions()
        all_results = []
        for p in all_preds:
            code = p["ma_chuong_trinh"]
            res = self.evaluate_single_major_chance(
                code,
                norm_scores,
                converted_en,
                request.priority_region,
                request.priority_group,
                major_data=p,
            )
            all_results.append(res)

        safety = [m for m in all_results if m.muc_do_an_toan == "RẤT_CAO"]
        target = [m for m in all_results if m.muc_do_an_toan == "CAO"]
        dream = [m for m in all_results if m.muc_do_an_toan == "TRUNG_BÌNH"]

        safety.sort(key=lambda x: x.xac_suat_trung_tuyen, reverse=True)
        target.sort(key=lambda x: x.xac_suat_trung_tuyen, reverse=True)
        dream.sort(key=lambda x: x.xac_suat_trung_tuyen, reverse=True)

        best_score = max(
            (m.tong_diem_xet_tuyen for m in all_results), default=0.0
        )
        best_combo = all_results[0].to_hop_toi_uu if all_results else "A00"
        p_score = all_results[0].diem_uu_tien if all_results else 0.0

        advice_list = [
            "Chiến lược 3 tầng bảo hiểm kim tự tháp:",
            "- Tầng 1 (Nguyện vọng ước mơ / Mạo hiểm): Đặt 1-2 ngành thuộc Giỏ Mạo hiểm ở NV1 - NV2 để nắm bắt cơ hội ngành yêu thích.",
            "- Tầng 2 (Nguyện vọng trọng tâm / Vừa sức): Đặt 2-3 ngành thuộc Giỏ Vừa sức ở NV3 - NV4 để nắm chắc cơ hội đỗ đại học đúng đam mê.",
            "- Tầng 3 (Nguyện vọng an toàn / Bảo hiểm): Đặt ít nhất 1 ngành thuộc Giỏ An toàn từ NV5 trở đi để phòng ngừa biến động điểm chuẩn bất ngờ.",
        ]

        return MajorRecommendationData(
            total_majors_evaluated=len(all_results),
            best_score=best_score,
            best_combination=best_combo,
            priority_score=p_score,
            safety_tier=StrategyTier(
                tier_name="Giỏ An toàn (Safety Tier)",
                tier_description="Điểm xét tuyển cao hơn điểm chuẩn dự kiến từ 0.8 điểm trở lên, xác suất đỗ trên 85%.",
                recommended_nv_slots="NV5 trở đi (Nguyện vọng bảo hiểm)",
                total_majors=len(safety),
                majors=safety,
            ),
            target_tier=StrategyTier(
                tier_name="Giỏ Vừa sức (Target Tier)",
                tier_description="Điểm xét tuyển tương đương hoặc nhỉnh hơn điểm chuẩn từ 0.2 - 0.7 điểm, xác suất đỗ 65% - 85%.",
                recommended_nv_slots="NV2 - NV4 (Nguyện vọng trọng tâm)",
                total_majors=len(target),
                majors=target,
            ),
            dream_tier=StrategyTier(
                tier_name="Giỏ Mạo hiểm / Thử thách (Dream Tier)",
                tier_description="Điểm xét tuyển sát dưới hoặc chênh lệch nhỏ trong biên độ dao động, xác suất đỗ 45% - 65%.",
                recommended_nv_slots="NV1 - NV2 (Nguyện vọng ước mơ)",
                total_majors=len(dream),
                majors=dream,
            ),
            strategic_advice=advice_list,
        )

    def configure_cold_start_major(
        self, request: ColdStartMajorRequest
    ) -> ColdStartMajorDetail:
        res = self.cold_start_engine.estimate_cold_start_major(
            ma_chuong_trinh=request.ma_chuong_trinh,
            ten_chuong_trinh=request.ten_chuong_trinh,
            cluster=request.cluster,
            faculty=request.faculty,
            degree_type=request.degree_type,
            chi_tieu=request.chi_tieu,
            external_ref_score=request.external_ref_score,
        )
        neighbors = [
            ColdStartNeighbor(
                cluster=n["cluster"],
                benchmark_base=n["benchmark_base"],
                similarity=n["similarity"],
                faculty=n["faculty"],
            )
            for n in res["nearest_neighbors"]
        ]
        return ColdStartMajorDetail(
            ma_chuong_trinh=res["ma_chuong_trinh"],
            ten_chuong_trinh=res["ten_chuong_trinh"],
            cluster=res["cluster"],
            estimated_cutoff=res["estimated_cutoff"],
            score_range_min=res["score_range_min"],
            score_range_max=res["score_range_max"],
            confidence_level=res["confidence_level"],
            nearest_neighbors=neighbors,
            recommendations=res["recommendations"],
        )

    def equate_percentile(
        self, request: PercentileEquatingRequest
    ) -> PercentileEquatingDetail:
        res = self.cold_start_engine.equate_subject_score(
            raw_score=request.raw_score,
            source_subject=request.source_subject,
            target_subject=request.target_subject,
        )
        return PercentileEquatingDetail(
            source_subject=res["source_subject"],
            raw_score=res["raw_score"],
            target_subject=res["target_subject"],
            z_score=res["z_score"],
            percentile=res["percentile"],
            equated_score=res["equated_score"],
        )


prediction_service = PredictionService()
