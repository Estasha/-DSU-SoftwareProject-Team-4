"""로컬 테스트용: 테이블 생성 + 샘플 데이터 삽입 (python -m app.seed_db)"""
from .db import Base, engine, SessionLocal
from .models import Region, SafetyScore, FacilityScore, TransitScore

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    if not db.query(Region).filter_by(name="해운대동").first():
        region = Region(name="해운대동", latitude=35.1631, longitude=129.1635)
        db.add(region)
        db.flush()

        db.add(SafetyScore(region_id=region.id, score=82.5))
        db.add(FacilityScore(region_id=region.id, score=74.0))
        db.add(TransitScore(region_id=region.id, score=90.0))
        db.commit()
        print("샘플 데이터 삽입 완료")
    else:
        print("이미 샘플 데이터가 존재합니다")

    for region in db.query(Region).all():
        print(
            region.name,
            region.safety_score.score if region.safety_score else None,
            region.facility_score.score if region.facility_score else None,
            region.transit_score.score if region.transit_score else None,
        )
finally:
    db.close()
