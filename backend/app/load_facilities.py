"""data/processed/facilities.csv를 DB의 facilities 테이블로 적재 (python -m app.load_facilities)"""
import csv
from pathlib import Path

from .db import Base, engine, SessionLocal
from .models import Facility

PROCESSED_CSV = Path(__file__).parent.parent.parent / "data" / "processed" / "facilities.csv"

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    with open(PROCESSED_CSV, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    for row in rows:
        exists = (
            db.query(Facility)
            .filter_by(
                facility_type=row["facility_type"],
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
            )
            .first()
        )
        if exists:
            continue
        db.add(
            Facility(
                category=row["category"],
                facility_type=row["facility_type"],
                name=row["name"] or None,
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                source=row["source"] or None,
            )
        )

    db.commit()
    print(f"완료: {len(rows)}건 중 적재 시도, 현재 facilities 총 {db.query(Facility).count()}건")
finally:
    db.close()
