"""지표별 점수를 가중합하여 종합 점수를 산출하는 로직.
가중치는 팀 논의로 확정되면 여기서 조정하면 됨 (지금은 임시값).
"""

WEIGHTS = {
    "safety": 0.4,
    "facility": 0.35,
    "transit": 0.25,
}


def calc_final_score(safety_score: float, facility_score: float, transit_score: float) -> float:
    final = (
        safety_score * WEIGHTS["safety"]
        + facility_score * WEIGHTS["facility"]
        + transit_score * WEIGHTS["transit"]
    )
    return round(final, 1)
