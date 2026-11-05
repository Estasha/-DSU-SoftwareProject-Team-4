"""주소/장소명 -> 좌표 변환 엔드포인트 (지도 이동용, 점수 계산과 무관)"""
from fastapi import APIRouter, HTTPException

from ..services.geocoding import geocode

router = APIRouter(prefix="/api", tags=["geocode"])


@router.get("/geocode")
def get_geocode(query: str):
    try:
        lat, lng = geocode(query)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    return {"lat": lat, "lng": lng}
