"""경찰서별 5대범죄 CSV 전처리 예시 스크립트.
data/raw/에 원본 CSV를 두고 실행하면 data/processed/에 정제 결과를 저장함.
"""
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"
MAPPING_DIR = Path(__file__).parent.parent / "mapping"


def main():
    df = pd.read_csv(RAW_DIR / "경찰서별_5대범죄.csv", encoding="cp949")

    # 정제
    df.columns = df.columns.str.strip()
    df["경찰서명"] = df["경찰서명"].str.replace("부산", "", regex=False).str.strip()
    df = df.fillna(0)
    df["총범죄건수"] = df["총범죄건수"].astype(int)

    # 매핑 (경찰서 관할구역 → 행정동)
    mapping = pd.read_csv(MAPPING_DIR / "경찰서_동_매핑표.csv")
    df = df.merge(mapping, on="경찰서명")

    # 정규화 (0~100점, 범죄가 적을수록 높은 점수)
    min_v, max_v = df["총범죄건수"].min(), df["총범죄건수"].max()
    df["안전점수"] = 100 - ((df["총범죄건수"] - min_v) / (max_v - min_v) * 100)

    PROCESSED_DIR.mkdir(exist_ok=True)
    df.to_csv(PROCESSED_DIR / "안전점수.csv", index=False, encoding="utf-8-sig")
    print(f"완료: {len(df)}개 지역 안전점수 계산됨")


if __name__ == "__main__":
    main()
