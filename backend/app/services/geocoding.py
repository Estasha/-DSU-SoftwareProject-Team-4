"""카카오 지오코딩 API 연동 — 주소/장소명을 위도/경도 좌표로 변환"""
import os
import requests

KAKAO_REST_KEY = os.getenv("KAKAO_REST_KEY")
KAKAO_ADDRESS_URL = "https://dapi.kakao.com/v2/local/search/address.json"
KAKAO_KEYWORD_URL = "https://dapi.kakao.com/v2/local/search/keyword.json"


def _search(url: str, query: str) -> list[dict]:
    headers = {"Authorization": f"KakaoAK {KAKAO_REST_KEY}"}
    res = requests.get(url, headers=headers, params={"query": query}, timeout=5)
    res.raise_for_status()
    return res.json().get("documents", [])


def geocode(address: str) -> tuple[float, float]:
    """주소/장소명 문자열을 (위도, 경도) 튜플로 변환. 실패 시 ValueError 발생.

    "사상구청"처럼 지번/도로명 주소가 아닌 장소명은 주소 검색 API로 찾을 수 없어서,
    주소 검색이 비면 키워드(장소) 검색으로 한 번 더 시도한다.
    """
    documents = _search(KAKAO_ADDRESS_URL, address)
    if not documents:
        documents = _search(KAKAO_KEYWORD_URL, address)
    if not documents:
        raise ValueError(f"'{address}'에 대한 좌표를 찾을 수 없습니다.")

    lat = float(documents[0]["y"])
    lng = float(documents[0]["x"])
    return lat, lng
