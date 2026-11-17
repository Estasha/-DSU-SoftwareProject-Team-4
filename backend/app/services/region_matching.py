"""좌표 -> 행정동(Region) 매칭

Region 테이블은 행정동별 경계(폴리곤)가 아니라 중심좌표 1개만 가지고 있어서,
입력 좌표와 가장 가까운 중심좌표를 가진 행정동을 찾는 방식으로 매칭한다.
"""
from math import radians, sin, cos, asin, sqrt

EARTH_RADIUS_M = 6371000


def _haversine_m(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    lat1, lng1, lat2, lng2 = map(radians, (lat1, lng1, lat2, lng2))
    dlat = lat2 - lat1
    dlng = lng2 - lng1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlng / 2) ** 2
    return 2 * EARTH_RADIUS_M * asin(sqrt(a))


def find_nearest_region(lat: float, lng: float, regions: list):
    """좌표 기준 가장 가까운 Region을 반환. regions가 비어있거나 좌표 없는 행만 있으면 None."""
    candidates = [r for r in regions if r.latitude is not None and r.longitude is not None]
    if not candidates:
        return None
    return min(candidates, key=lambda r: _haversine_m(lat, lng, r.latitude, r.longitude))
