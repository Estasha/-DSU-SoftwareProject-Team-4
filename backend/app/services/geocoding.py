"""카카오 지오코딩 API 연동 — 주소를 위도/경도 좌표로 변환"""
import os
import requests

KAKAO_REST_KEY = os.getenv("KAKAO_REST_KEY")
KAKAO_GEOCODE_URL = "https://dapi.kakao.com/v2/local/search/address.json"


def geocode(address: str) -> tuple[float, float]:
    """주소 문자열을 (위도, 경도) 튜플로 변환. 실패 시 ValueError 발생."""
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}
    res = requests.get(KAKAO_GEOCODE_URL, headers=headers, params={"query": address}, timeout=5)
    res.raise_for_status()
    data = res.json()

    documents = data.get("documents")
    if not documents:
        raise ValueError(f"'{address}'에 대한 좌표를 찾을 수 없습니다.")

    lat = float(documents[0]["y"])
    lng = float(documents[0]["x"])
    return lat, lng
