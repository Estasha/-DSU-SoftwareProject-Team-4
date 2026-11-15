"""시설 유형별 점수 가중치 표 (docs/동네 진단 서비스 정주여건 점수 계산 방식.md 의 '파라미터 초안').

가중치는 시설 행(facilities 테이블)에 저장하지 않고 여기서 facility_type으로 찾는다.
값을 바꿀 때 DB를 다시 적재할 필요 없이 이 표만 고치면 된다.
표에 없는 유형은 점수 계산에서 제외된다(예: 철물 소매, 의류 소매).
"""

# 점수 카테고리 (지도 레이어용 facilities.category와는 별개 개념)
SAFETY = "안전"
CLINIC = "의료_의원급"
GENERAL_HOSPITAL = "의료_종합병원"  # 개수가 아니라 최근접 거리로 계산
DAILY_STORE = "생필품"
BUS = "버스"
SUBWAY = "지하철"

# facility_type -> (점수 카테고리, 유형 가중치)
FACILITY_WEIGHTS: dict[str, tuple[str, float]] = {
    "cctv": (SAFETY, 1.0),  # 현재 데이터는 전부 방범용 CCTV 데이터셋
    "내과/소아과 의원": (CLINIC, 0.6),
    "피부/비뇨기과 의원": (CLINIC, 0.1),
    "성형외과 의원": (CLINIC, 0.1),
    "종합병원": (GENERAL_HOSPITAL, 1.0),
    "슈퍼마켓": (DAILY_STORE, 1.0),
    "편의점": (DAILY_STORE, 1.0),
    "약국": (DAILY_STORE, 1.0),
    "버스정류장": (BUS, 1.0),  # 경유 노선 수는 고려하지 않음
    "지하철역": (SUBWAY, 1.0),
}


def get_weight(facility_type: str) -> tuple[str, float] | None:
    """(점수 카테고리, 가중치)를 돌려준다. 점수 계산 대상이 아니면 None."""
    return FACILITY_WEIGHTS.get(facility_type)
