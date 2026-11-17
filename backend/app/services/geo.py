"""좌표 간 거리 계산 (지도 클릭 지점 기준 반경 검색용)"""
from math import radians, sin, cos, asin, sqrt

EARTH_RADIUS_M = 6371000


def haversine_distance_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """두 좌표(위도/경도) 사이의 직선 거리를 미터 단위로 계산."""
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    d_lat = lat2 - lat1
    d_lng = lng2 - lng1
    a = sin(d_lat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(d_lng / 2) ** 2
    return 2 * EARTH_RADIUS_M * asin(sqrt(a))
