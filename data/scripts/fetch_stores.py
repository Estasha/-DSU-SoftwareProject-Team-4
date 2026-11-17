"""소상공인시장진흥공단_상가(상권)정보 API에서 사상구 전체 상가업소 데이터를 받아
data/raw/사상구_상가업소정보.csv 로 저장한다.

실행: python data/scripts/fetch_stores.py
(backend/.env의 DATA_GO_KR_KEY를 사용)
"""
import os
import time
from pathlib import Path

import pandas as pd
import requests
from dotenv import load_dotenv

RAW_DIR = Path(__file__).parent.parent / "raw"
BACKEND_ENV = Path(__file__).parent.parent.parent / "backend" / ".env"
load_dotenv(BACKEND_ENV)

API_KEY = os.getenv("DATA_GO_KR_KEY")
URL = "https://apis.data.go.kr/B553077/api/open/sdsc2/storeListInDong"
SASANG_SIGNGU_CD = "26530"
NUM_OF_ROWS = 1000


def fetch_all():
    rows = []
    page = 1
    while True:
        params = {
            "serviceKey": API_KEY,
            "divId": "signguCd",
            "key": SASANG_SIGNGU_CD,
            "type": "json",
            "numOfRows": NUM_OF_ROWS,
            "pageNo": page,
        }
        res = requests.get(URL, params=params, timeout=20)
        res.raise_for_status()
        body = res.json()["body"]
        items = body["items"]
        rows.extend(items)
        print(f"  page {page}: {len(items)}건 (누적 {len(rows)}/{body['totalCount']})")

        if len(rows) >= body["totalCount"] or not items:
            break
        page += 1
        time.sleep(0.2)  # API 과부하 방지

    return rows


def main():
    if not API_KEY:
        print("DATA_GO_KR_KEY가 backend/.env에 없습니다.")
        return

    rows = fetch_all()
    df = pd.DataFrame(rows)

    RAW_DIR.mkdir(exist_ok=True)
    out_path = RAW_DIR / "사상구_상가업소정보.csv"
    df.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"완료: {len(df)}건 저장됨 -> {out_path}")


if __name__ == "__main__":
    main()
