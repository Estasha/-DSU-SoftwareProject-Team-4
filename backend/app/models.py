"""SQLAlchemy 테이블 정의 (DB 스키마 확정되면 이 파일을 채워나가면 됨)"""
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from .db import Base


class Region(Base):
    """행정동 기준 지역 테이블"""
    __tablename__ = "regions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)  # 예: "해운대동"
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)

    safety_score = relationship("SafetyScore", back_populates="region", uselist=False)
    facility_score = relationship("FacilityScore", back_populates="region", uselist=False)
    transit_score = relationship("TransitScore", back_populates="region", uselist=False)


class SafetyScore(Base):
    __tablename__ = "safety_scores"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)  # 0~100 정규화된 점수

    region = relationship("Region", back_populates="safety_score")


class FacilityScore(Base):
    __tablename__ = "facility_scores"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)

    region = relationship("Region", back_populates="facility_score")


class TransitScore(Base):
    __tablename__ = "transit_scores"

    id = Column(Integer, primary_key=True, index=True)
    region_id = Column(Integer, ForeignKey("regions.id"), unique=True, nullable=False)
    score = Column(Float, nullable=False)

    region = relationship("Region", back_populates="transit_score")


class Facility(Base):
    """위치 기반 시설 공통 테이블 (CCTV, 어린이집, 병원 등).

    행정동 단위로 집계하는 위 Score 테이블들과 달리, 지도 클릭 지점 기준
    반경 검색(예: 방범지도)에 쓰기 위해 개별 시설의 위도/경도를 그대로 저장한다.
    데이터셋마다 컬럼명이 달라도 data/scripts/clean_facilities.py에서
    이 스키마(category, facility_type, name, latitude, longitude)로 통일해서 적재한다.
    """
    __tablename__ = "facilities"

    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, nullable=False, index=True)  # "안전" | "생활편의"
    facility_type = Column(String, nullable=False, index=True)  # "cctv" | "어린이집" | "병원" 등
    name = Column(String, nullable=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    source = Column(String, nullable=True)  # 원본 데이터셋명 (출처 추적용)
