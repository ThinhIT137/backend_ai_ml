import math
from typing import Any, Dict, List, Optional, Tuple
import numpy as np


class DynamicPredictor:
    def __init__(self):
        self.commitment_weights = {
            1: 1.0,
            2: 0.7,
            3: 0.45,
            4: 0.3,
            5: 0.2,
        }
        self.default_nv_weight = 0.15

    def get_commitment_weight(self, nguyện_vọng: int) -> float:
        return self.commitment_weights.get(int(nguyện_vọng), self.default_nv_weight)

    def estimate_influx_ratio(
        self, days_elapsed: int, total_days: int = 60, k: float = 0.12
    ) -> float:
        t = max(0, min(days_elapsed, total_days))
        mid = total_days / 2.0
        ratio = 1.0 / (1.0 + math.exp(-k * (t - mid)))
        return float(np.clip(ratio, 0.05, 1.0))

    def filter_and_weight_applications(
        self, applications: List[Dict[str, Any]]
    ) -> List[Tuple[float, float]]:
        weighted_scores = []
        for app in applications:
            score = float(app.get("tong_diem", 0.0))
            nv = int(app.get("nguyen_vong", 1))
            weight = self.get_commitment_weight(nv)
            if score > 0.0:
                weighted_scores.append((score, weight))
        weighted_scores.sort(key=lambda x: x[0], reverse=True)
        return weighted_scores

    def calculate_empirical_cutoff(
        self,
        weighted_scores: List[Tuple[float, float]],
        quota: int,
        influx_ratio: float = 1.0,
    ) -> float:
        if not weighted_scores or quota <= 0:
            return 24.0

        target_quota = float(quota)
        effective_quota = target_quota * max(0.05, influx_ratio)

        cum_weight = 0.0
        for score, weight in weighted_scores:
            cum_weight += weight
            if cum_weight >= effective_quota:
                return round(float(score), 2)

        return round(float(weighted_scores[-1][0]), 2)

    def calculate_bayes_dynamic_cutoff(
        self,
        prior_cutoff: float,
        empirical_cutoff: float,
        applicant_count: int,
        quota: int,
        news_delta: float = 0.0,
        shrinkage_factor: float = 0.4,
        max_evidence_weight: float = 0.40,
    ) -> Tuple[float, float]:
        safe_quota = max(1, quota)
        smoothing_const = safe_quota * 0.5
        w_raw = applicant_count / (applicant_count + smoothing_const)
        w_t = float(np.clip(w_raw, 0.0, max_evidence_weight))

        bounded_news_delta = float(np.clip(news_delta, -2.0, 2.0)) * shrinkage_factor
        blended = (1.0 - w_t) * prior_cutoff + w_t * empirical_cutoff + bounded_news_delta
        final_cutoff = float(np.clip(blended, 14.0, 30.0))

        return round(final_cutoff, 2), round(w_t, 3)

    def build_trend_timeline(
        self,
        prior_cutoff: float,
        historical_applications: List[Dict[str, Any]],
        quota: int,
        total_days: int = 30,
        news_delta: float = 0.0,
        max_evidence_weight: float = 0.40,
    ) -> List[Dict[str, Any]]:
        timeline = []
        apps_by_day = {}
        for app in historical_applications:
            day = int(app.get("day_offset", 1))
            apps_by_day.setdefault(day, []).append(app)

        accumulated = []
        for d in range(1, total_days + 1):
            if d in apps_by_day:
                accumulated.extend(apps_by_day[d])

            influx_ratio = self.estimate_influx_ratio(d, total_days)
            weighted_scores = self.filter_and_weight_applications(accumulated)
            empirical = self.calculate_empirical_cutoff(
                weighted_scores, quota, influx_ratio
            )
            dyn_cutoff, weight_evidence = self.calculate_bayes_dynamic_cutoff(
                prior_cutoff=prior_cutoff,
                empirical_cutoff=empirical,
                applicant_count=len(accumulated),
                quota=quota,
                news_delta=news_delta,
                max_evidence_weight=max_evidence_weight,
            )

            timeline.append(
                {
                    "day_offset": d,
                    "total_applicants": len(accumulated),
                    "empirical_cutoff": empirical,
                    "predicted_cutoff": dyn_cutoff,
                    "weight_evidence": weight_evidence,
                }
            )

        return timeline


dynamic_predictor = DynamicPredictor()
