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

    BATCH_SIZE = 300  # 한 번에 너무 많이 넣으면 Turso 연결이 끊김(Hrana 오류) - 나눠서 커밋

    if replace:
        db.query(Facility).delete()
        db.commit()
        print("--replace: 기존 facilities 삭제 완료")

    added = 0
    pending = []
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
        pending.append(
            Facility(
                category=row["category"],
                facility_type=row["facility_type"],
                name=row["name"] or None,
                latitude=float(row["latitude"]),
                longitude=float(row["longitude"]),
                source=row["source"] or None,
            )
        )
        if len(pending) >= BATCH_SIZE:
            db.add_all(pending)
            db.commit()
            added += len(pending)
            print(f"  {added}건 커밋됨...")
            pending = []

    if pending:
        db.add_all(pending)
        db.commit()
        added += len(pending)

    print(f"완료: CSV {len(rows)}건 처리, {added}건 추가, 현재 facilities 총 {db.query(Facility).count()}건")
finally:
    db.close()
