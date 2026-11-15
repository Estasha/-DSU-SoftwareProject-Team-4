"""data/processed/facilities.csv를 DB의 facilities 테이블로 적재

    python -m app.load_facilities            # 이미 있는 시설(같은 유형·좌표)은 건너뛰고 추가만
    python -m app.load_facilities --replace  # facilities 테이블을 비우고 CSV 내용으로 전부 다시 넣음
"""
import csv
import sys
from pathlib import Path

from .db import Base, engine, SessionLocal
from .models import Facility

PROCESSED_CSV = Path(__file__).parent.parent.parent / "data" / "processed" / "facilities.csv"

replace = "--replace" in sys.argv

Base.metadata.create_all(bind=engine)

db = SessionLocal()
try:
    with open(PROCESSED_CSV, encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))

    if replace:
        deleted = db.query(Facility).delete()
        print(f"--replace: 기존 facilities {deleted}건 삭제")

    for row in rows:
        if not replace:
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
    print(f"완료: CSV {len(rows)}건 처리, 현재 facilities 총 {db.query(Facility).count()}건")
finally:
    db.close()
