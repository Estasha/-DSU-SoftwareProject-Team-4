"""Pydantic 요청/응답 모델 — API가 주고받는 데이터의 '모양'을 검증"""
from pydantic import BaseModel


class ScoreResponse(BaseModel):
    region: str
    safety_score: float
    facility_score: float
    transit_score: float
    final_score: float

    class Config:
        from_attributes = True
