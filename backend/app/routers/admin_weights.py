"""관리자 페이지에서 점수 가중치를 조회/수정하는 엔드포인트.

인증은 아직 없음 — 현재 관리자 메뉴 전체가 프론트엔드 비밀번호 확인뿐이라
(AdminPage.jsx 참고, FR-08 코드 주석에도 명시된 한계) 같은 수준으로 맞춰둠.
실제 운영 전환 시 서버 쪽 인증을 추가해야 함.

카테고리 가중치(W_c)·시설 유형 가중치(wᵢ)는 페르소나(개인/가족/노인)별로 따로 저장된다.
반경(r_c)·목표 개수(n_c)는 페르소나와 무관한 공통 값이라 persona 구분이 없다.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..db import get_db
from ..models import CategoryParam, PersonaCategoryWeight, PersonaFacilityTypeWeight
from ..schemas import (
    CategoryParamOut,
    CategoryParamUpdate,
    CategoryWeightUpdate,
    FacilityTypeWeightUpdate,
    PersonaCategoryWeightOut,
    PersonaFacilityTypeWeightOut,
)

router = APIRouter(prefix="/api/admin/weights", tags=["admin-weights"])


@router.get("/categories", response_model=list[CategoryParamOut])
def list_category_params(db: Session = Depends(get_db)):
    """반경(r_c)·목표 개수(n_c) — 페르소나 공통."""
    return db.query(CategoryParam).all()


@router.put("/categories/{score_category}", response_model=CategoryParamOut)
def update_category_param(score_category: str, body: CategoryParamUpdate, db: Session = Depends(get_db)):
    param = db.query(CategoryParam).filter(CategoryParam.score_category == score_category).first()
    if not param:
        raise HTTPException(status_code=404, detail="해당 카테고리가 없습니다.")

    if body.radius_m is not None:
        param.radius_m = body.radius_m
    if body.target_count is not None:
        param.target_count = body.target_count

    db.commit()
    db.refresh(param)
    return param


@router.get("/personas/{persona}/categories", response_model=list[PersonaCategoryWeightOut])
def list_persona_category_weights(persona: str, db: Session = Depends(get_db)):
    """카테고리 가중치(W_c) — 페르소나별."""
    return db.query(PersonaCategoryWeight).filter(PersonaCategoryWeight.persona == persona).all()


@router.put("/personas/{persona}/categories/{score_category}", response_model=PersonaCategoryWeightOut)
def update_persona_category_weight(
    persona: str, score_category: str, body: CategoryWeightUpdate, db: Session = Depends(get_db)
):
    weight = (
        db.query(PersonaCategoryWeight)
        .filter(PersonaCategoryWeight.persona == persona, PersonaCategoryWeight.score_category == score_category)
        .first()
    )
    if not weight:
        raise HTTPException(status_code=404, detail="해당 페르소나·카테고리 조합이 없습니다.")

    weight.category_weight = body.category_weight
    db.commit()
    db.refresh(weight)
    return weight


@router.get("/personas/{persona}/facility-types", response_model=list[PersonaFacilityTypeWeightOut])
def list_persona_facility_type_weights(persona: str, db: Session = Depends(get_db)):
    """시설 유형 가중치(wᵢ) — 페르소나별."""
    return db.query(PersonaFacilityTypeWeight).filter(PersonaFacilityTypeWeight.persona == persona).all()


@router.put("/personas/{persona}/facility-types/{facility_type}", response_model=PersonaFacilityTypeWeightOut)
def update_persona_facility_type_weight(
    persona: str, facility_type: str, body: FacilityTypeWeightUpdate, db: Session = Depends(get_db)
):
    weight = (
        db.query(PersonaFacilityTypeWeight)
        .filter(
            PersonaFacilityTypeWeight.persona == persona,
            PersonaFacilityTypeWeight.facility_type == facility_type,
        )
        .first()
    )
    if not weight:
        raise HTTPException(status_code=404, detail="해당 페르소나·시설 유형 조합이 없습니다.")

    weight.weight = body.weight
    db.commit()
    db.refresh(weight)
    return weight
