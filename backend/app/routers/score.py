"""점수 조회 관련 엔드포인트"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from .. import models
from ..schemas import ScoreResponse
from ..services.geocoding import geocode
from ..services.scoring import calc_final_score

router = APIRouter(prefix="/api", tags=["score"])


@router.get("/score", response_model=ScoreResponse)
def get_score(address: str, db: Session = Depends(get_db)):
    """주소를 받아 해당 지역의 종합 점수를 반환.

    흐름: 주소 → 좌표(지오코딩) → 지역 매칭 → 지표별 점수 조회 → 가중합 계산
    지역 매칭 로직(좌표 → 행정동)은 DB 스키마 확정 후 구현 필요.
    """
    try:
        lat, lng = geocode(address)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))

    # TODO: 좌표(lat, lng) 기준으로 소속 행정동(Region)을 찾는 로직 구현
    region = db.query(models.Region).first()
    if not region:
        raise HTTPException(status_code=404, detail="일치하는 지역 데이터가 없습니다.")

    safety = region.safety_score.score if region.safety_score else 0
    facility = region.facility_score.score if region.facility_score else 0
    transit = region.transit_score.score if region.transit_score else 0
    final = calc_final_score(safety, facility, transit)

    return ScoreResponse(
        region=region.name,
        safety_score=safety,
        facility_score=facility,
        transit_score=transit,
        final_score=final,
    )
