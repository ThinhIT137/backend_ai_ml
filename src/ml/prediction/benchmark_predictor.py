import json
import os
import joblib
import numpy as np
import pandas as pd


class BenchmarkPredictor:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.assets_dir = os.path.join(self.base_dir, "assets")
        self.model = None
        self.metadata = {}
        self.conversion_data = {}
        self.anchors = {}
        self.load_assets()

    def load_assets(self):
        model_path = os.path.join(self.assets_dir, "huber_regressor_2026.joblib")
        if os.path.exists(model_path):
            self.model = joblib.load(model_path)

        meta_path = os.path.join(self.assets_dir, "model_metadata.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                self.metadata = json.load(f)

        conv_path = os.path.join(self.assets_dir, "conversion_scales_2026.json")
        if os.path.exists(conv_path):
            with open(conv_path, "r", encoding="utf-8") as f:
                self.conversion_data = json.load(f)

        anchor_path = os.path.join(self.assets_dir, "hanoi_anchor_2025_2026.json")
        if os.path.exists(anchor_path):
            with open(anchor_path, "r", encoding="utf-8") as f:
                raw_list = json.load(f)
                self.anchors = {
                    item["ma_chuong_trinh_2026"]: item for item in raw_list
                }

    def convert_thpt_to_all_methods(self, thpt_score: float) -> dict:
        thpt_score = float(np.clip(thpt_score, 14.0, 30.0))

        hb_score = None
        for row in self.conversion_data.get("hoc_ba_to_thpt", []):
            if row["thpt_min"] <= thpt_score <= row["thpt_max"]:
                span = max(0.01, row["thpt_max"] - row["thpt_min"])
                ratio = (thpt_score - row["thpt_min"]) / span
                hb_score = (
                    row["hoc_ba_min"] + ratio * (row["hoc_ba_max"] - row["hoc_ba_min"])
                )
                break
        if hb_score is None:
            hb_score = np.clip(thpt_score + 1.8, 18.0, 30.0)

        tsa_score = None
        for row in self.conversion_data.get("tsa_to_thpt", []):
            if row["thpt_min"] <= thpt_score <= row["thpt_max"]:
                span = max(0.01, row["thpt_max"] - row["thpt_min"])
                ratio = (thpt_score - row["thpt_min"]) / span
                tsa_score = (
                    row["tsa_min"] + ratio * (row["tsa_max"] - row["tsa_min"])
                )
                break
        if tsa_score is None:
            tsa_score = np.clip(thpt_score * 2.2, 35.0, 100.0)

        hsa_score = None
        for row in self.conversion_data.get("hsa_to_thpt", []):
            if row["thpt_min"] <= thpt_score <= row["thpt_max"]:
                span = max(0.01, row["thpt_max"] - row["thpt_min"])
                ratio = (thpt_score - row["thpt_min"]) / span
                hsa_score = (
                    row["hsa_min"] + ratio * (row["hsa_max"] - row["hsa_min"])
                )
                break
        if hsa_score is None:
            hsa_score = np.clip(thpt_score * 3.5, 50.0, 150.0)

        return {
            "pt1_thpt": round(float(thpt_score), 2),
            "pt2_hoc_ba": round(float(hb_score), 2),
            "pt3_hsa": round(float(hsa_score), 2),
            "pt4_tsa": round(float(tsa_score), 2),
        }

    def predict_scenario(
        self,
        ma_chuong_trinh: str,
        custom_quota_growth: float = None,
        custom_macro_delta: float = None,
    ) -> float:
        if not self.model or ma_chuong_trinh not in self.anchors:
            return 24.0

        anchor = self.anchors[ma_chuong_trinh]
        c25 = float(anchor.get("diem_chuan_2025_pt1") or 23.0)
        q25 = float(anchor.get("chi_tieu_2025") or 60)
        q26 = float(anchor.get("chi_tieu_2026") or 60)

        if custom_quota_growth is not None:
            q_growth = float(custom_quota_growth)
        else:
            q_growth = (q26 - q25) / max(1.0, q25)

        combos = anchor.get("to_hop_xet_tuyen", ["A00"])
        primary_combo = combos[0] if combos else "A00"
        combo_map = {
            "A00": -0.34,
            "A01": -0.87,
            "B00": 0.65,
            "C00": -2.97,
            "C01": -1.06,
            "D01": 0.06,
            "D07": 0.78,
            "D09": 0.18,
            "D10": -1.53,
            "X06": -0.46,
        }
        if custom_macro_delta is not None:
            macro_delta = float(custom_macro_delta)
        else:
            macro_delta = combo_map.get(primary_combo, -0.34)

        sim_pred = c25 + macro_delta - (q_growth * 0.4)

        name = anchor.get("ten_chuong_trinh", "").lower()
        is_clc = 1.0 if ("qt" in ma_chuong_trinh.lower() or "clc" in name) else 0.0
        is_railway = 1.0 if ("ds" in ma_chuong_trinh.lower() or "đường sắt" in name) else 0.0
        is_semiconductor = (
            1.0
            if (
                "bd" in ma_chuong_trinh.lower()
                or "bán dẫn" in name
                or "vi mạch" in name
            )
            else 0.0
        )
        is_english = 1.0 if ma_chuong_trinh == "GHA01" else 0.0

        cluster = self.determine_cluster(ma_chuong_trinh)
        cls_econ = 1.0 if cluster == "ECONOMICS_TRANSPORT" else 0.0
        cls_elec = 1.0 if cluster == "ELECTRICAL_AUTOMATION" else 0.0
        cls_it = 1.0 if cluster == "IT_CS" else 0.0
        cls_mech = 1.0 if cluster == "MECHANICAL_AUTO" else 0.0

        features = np.array(
            [
                [
                    c25,
                    q_growth,
                    sim_pred,
                    macro_delta,
                    is_clc,
                    is_railway,
                    is_semiconductor,
                    is_english,
                    cls_econ,
                    cls_elec,
                    cls_it,
                    cls_mech,
                ]
            ]
        )

        feature_names = self.metadata.get("feature_names")
        if feature_names:
            features = pd.DataFrame(features, columns=feature_names)

        pred = float(self.model.predict(features)[0])
        pred = round(float(np.clip(pred, 15.0, 29.5)), 2)
        return pred

    def determine_cluster(self, code: str) -> str:
        clusters = {
            "IT_CS": ["GHA02", "GHA13", "GHA14", "GHA14QT", "GHA15", "GHA24", "GHA33"],
            "MECHANICAL_AUTO": [
                "GHA16",
                "GHA16QT",
                "GHA17",
                "GHA18",
                "GHA19",
                "GHA19DS",
                "GHA20",
                "GHA20QT",
            ],
            "ELECTRICAL_AUTOMATION": [
                "GHA21",
                "GHA21DS",
                "GHA22",
                "GHA22BD",
                "GHA22QT",
                "GHA23",
                "GHA23DS",
                "GHA23TM",
            ],
            "ECONOMICS_TRANSPORT": [
                "GHA01",
                "GHA03",
                "GHA04",
                "GHA04QT",
                "GHA05",
                "GHA06",
                "GHA06QT",
                "GHA07",
                "GHA08",
                "GHA08DS",
                "GHA09",
                "GHA10",
                "GHA10QT",
            ],
        }
        for cname, codes in clusters.items():
            if code in codes:
                return cname
        return "CIVIL_INFRASTRUCTURE"

    def determine_trend(self, delta: float) -> str:
        if delta >= 0.3:
            return "TĂNG"
        if delta <= -0.3:
            return "GIẢM"
        return "ỔN_ĐỊNH"

    def get_influencing_factors(self, code: str, delta: float) -> list:
        factors = []
        name = self.anchors.get(code, {}).get("ten_chuong_trinh", "").lower()

        if "ds" in code.lower() or "đường sắt" in name:
            factors.append("Quy hoạch phát triển đường sắt tốc độ cao quốc gia")
        if "bd" in code.lower() or "bán dẫn" in name or "vi mạch" in name:
            factors.append("Định hướng chiến lược phát triển công nghiệp vi mạch bán dẫn")
        if code == "GHA01":
            factors.append("Biến động phổ điểm thi tốt nghiệp THPT môn Tiếng Anh nhân hệ số 2")
        if "logistics" in name or "kinh tế" in name:
            factors.append("Nhu cầu thị trường lao động chuỗi cung ứng và kinh tế số")
        if "trí tuệ nhân tạo" in name or "công nghệ thông tin" in name:
            factors.append("Sức hút ngành công nghệ chiến lược và trí tuệ nhân tạo")

        if delta > 0.5:
            factors.append("Tăng trưởng mạnh tỉ lệ cạnh tranh và nguyện vọng đăng ký")
        elif delta < -0.5:
            factors.append("Độ lệch giảm phổ điểm tổ hợp thi tốt nghiệp THPT")
        else:
            factors.append("Điểm chuẩn mỏ neo năm 2025 duy trì độ ổn định cao")

        return factors


benchmark_predictor = BenchmarkPredictor()
