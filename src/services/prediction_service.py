from typing import List, Optional
from src.core.exceptions import NotFoundException
from src.ml.prediction.benchmark_predictor import benchmark_predictor
from src.repositories.prediction_repository import prediction_repository
from src.schemas.prediction_schema import (
    BenchmarkPredictionItem,
    BenchmarkScenarioRequest,
    EquivalentMethodScores,
)


class PredictionService:
    def __init__(self):
        self.repo = prediction_repository
        self.predictor = benchmark_predictor

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


prediction_service = PredictionService()