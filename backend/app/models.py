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
