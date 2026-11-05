"""사상구청 홈페이지에 수동으로 나열된 노인교실 목록(공공데이터 없음)을
카카오 지오코딩으로 좌표 변환해서 data/processed/사상구_노인교실.csv 로 저장.
출처: https://www.sasang.go.kr (최종수정일 2025-08-11 기준, 2026-11-05 확인)
휴관 중인 시설(사상교회부설 노인대학, 2025년 휴관)은 제외함.

실행: python data/scripts/geocode_senior_classrooms.py
(backend/.env의 KAKAO_REST_KEY 사용)
"""
import sys
import time
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv

BACKEND_DIR = Path(__file__).parent.parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))
load_dotenv(BACKEND_DIR / ".env")

from app.services.geocoding import geocode  # noqa: E402

PROCESSED_DIR = Path(__file__).parent.parent / "processed"

# (시설명, 주소) — "부산광역시" 접두사는 지오코딩 정확도를 위해 붙임
FACILITIES = [
    ("모라종합사회복지관 부설노인복지대학", "부산광역시 사상구 모라로110번길 129"),
    ("백양종합사회복지관 부설노인교실", "부산광역시 사상구 모라로192번길 20-33"),
    ("모라교회부설 모라노인(상록)교실", "부산광역시 사상구 모덕로95번길 101"),
    ("대한노인회 사상구지회 부설노인대학", "부산광역시 사상구 사상로319번길 6"),
    ("감전교회부설 감전어르신교실", "부산광역시 사상구 괘감로 77"),
    ("사상노인대학", "부산광역시 사상구 새벽로 172"),
    ("사상구종합사회복지관 다솜노인대학", "부산광역시 사상구 백양대로 527"),
    ("학장종합사회복지관 천수어르신교실", "부산광역시 사상구 학감대로49번길 28-70"),
    ("충성교회부설 노인대학", "부산광역시 사상구 모라로110번길 40-121"),
    # 사상교회부설 노인대학 - 2025년 휴관으로 제외
]


def main():
    rows = []
    for name, address in FACILITIES:
        try:
            lat, lng = geocode(address)
            rows.append({"name": name, "address": address, "latitude": lat, "longitude": lng})
            print(f"  OK: {name} -> ({lat}, {lng})")
        except Exception as e:
            print(f"  실패: {name} ({address}) - {e}")
        time.sleep(0.2)

    df = pd.DataFrame(rows)
    PROCESSED_DIR.mkdir(exist_ok=True)
    out_path = PROCESSED_DIR / "사상구_노인교실.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"완료: {len(df)}/{len(FACILITIES)}건 저장됨 -> {out_path}")


if __name__ == "__main__":
    main()
