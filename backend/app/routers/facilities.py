"""방범지도 등 반경 기반 시설 조회 엔드포인트"""
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..schemas import NearbyFacilitiesResponse, FacilityOut
from ..services.geo import haversine_distance_m

router = APIRouter(prefix="/api/facilities", tags=["facilities"])


@router.get("/nearby", response_model=NearbyFacilitiesResponse)
def get_nearby_facilities(
    lat: float,
    lng: float,
    radius_m: float = 100,
    facility_type: str | None = Query(default=None, description="예: cctv, 소매 (생략하면 전체 종류)"),
    category: str | None = Query(default=None, description="예: 안전, 생활편의, 음식점 (생략하면 전체)"),
    db: Session = Depends(get_db),
):
    """클릭한 좌표(lat, lng) 기준 반경(radius_m) 안에 있는 시설 개수와 목록을 반환."""
    query = db.query(models.Facility)
    if facility_type:
        query = query.filter(models.Facility.facility_type == facility_type)
    if category:
        query = query.filter(models.Facility.category == category)

    nearby = []
    for facility in query.all():
        distance = haversine_distance_m(lat, lng, facility.latitude, facility.longitude)
        if distance <= radius_m:
            nearby.append(
                FacilityOut(
                    name=facility.name,
                    facility_type=facility.facility_type,
                    latitude=facility.latitude,
                    longitude=facility.longitude,
                    distance_m=round(distance, 1),
                )
            )

    nearby.sort(key=lambda f: f.distance_m)
    return NearbyFacilitiesResponse(count=len(nearby), facilities=nearby)
