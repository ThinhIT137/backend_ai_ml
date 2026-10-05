from typing import List, Optional
from src.core.exceptions import NotFoundException
from src.ml.prediction.admission_predictor import admission_predictor
from src.ml.prediction.benchmark_predictor import benchmark_predictor
from src.repositories.prediction_repository import prediction_repository
from src.schemas.prediction_schema import (
    AdmissionChanceRequest,
    BenchmarkPredictionItem,
    BenchmarkScenarioRequest,
    EquivalentMethodScores,
    MajorChanceResult,
    MajorRecommendationData,
    StrategyTier,
)


class PredictionService:
    def __init__(self):
        self.repo = prediction_repository
        self.predictor = benchmark_predictor
        self.evaluator = admission_predictor

    def build_item(self, row: dict) -> BenchmarkPredictionItem:
        code = row["ma_chuong_trinh"]
        pred_score = round(float(row["diem_du_doan"]), 2)
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

    def evaluate_single_major_chance(
        self,
        code: str,
        norm_scores: dict,
        converted_en: float,
        region: Optional[str],
        group: Optional[str],
    ) -> MajorChanceResult:
        row = self.repo.get_2026_prediction_by_major(code)
        major_name = row["ten_chuong_trinh"] if row else code
        cutoff = row["diem_du_doan"] if row else 24.0

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

        return self.evaluate_single_major_chance(
            target_code,
            norm_scores,
            converted_en,
            request.priority_region,
            request.priority_group,
        )

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


prediction_service = PredictionService()