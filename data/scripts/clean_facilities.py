"""위치 기반 시설 데이터(CCTV, 어린이집, 병원 등) 공통 전처리 틀.

공공데이터포털 데이터셋마다 컬럼명이 제각각이라(위도/경도, LAT/LOT, Y좌표/X좌표 등),
이 파일에서 공통 스키마(category, facility_type, name, latitude, longitude, source)로
통일해서 data/processed/facilities.csv 에 누적 저장한다.

새 데이터셋을 추가하려면:
1. data/raw/ 에 원본 CSV를 둔다
2. standardize()로 컬럼명을 공통 스키마로 맞춘 DataFrame을 만든다
3. main()의 SOURCES 리스트에 그 처리 결과를 추가한다
"""
import pandas as pd
from pathlib import Path

RAW_DIR = Path(__file__).parent.parent / "raw"
PROCESSED_DIR = Path(__file__).parent.parent / "processed"

# 공공데이터에서 자주 쓰이는 위도/경도 컬럼명 별칭 (필요시 계속 추가)
LATITUDE_ALIASES = ["위도", "lat", "LAT", "Y좌표", "y좌표"]
LONGITUDE_ALIASES = ["경도", "lot", "LOT", "lng", "X좌표", "x좌표"]


def _find_column(df: pd.DataFrame, aliases: list[str]) -> str:
    for alias in aliases:
        if alias in df.columns:
            return alias
    raise KeyError(f"다음 별칭 중 일치하는 컬럼을 찾지 못함: {aliases} (실제 컬럼: {list(df.columns)})")


def standardize(
    df: pd.DataFrame,
    category: str,
    facility_type: str,
    source: str,
    name_col: str | None = None,
    lat_col: str | None = None,
    lng_col: str | None = None,
) -> pd.DataFrame:
    """원본 DataFrame을 공통 스키마(category/facility_type/name/latitude/longitude/source)로 변환."""
    lat_col = lat_col or _find_column(df, LATITUDE_ALIASES)
    lng_col = lng_col or _find_column(df, LONGITUDE_ALIASES)

    result = pd.DataFrame({
        "category": category,
        "facility_type": facility_type,
        "name": df[name_col] if name_col else None,
        "latitude": pd.to_numeric(df[lat_col], errors="coerce"),
        "longitude": pd.to_numeric(df[lng_col], errors="coerce"),
        "source": source,
    })

    before = len(result)
    result = result.dropna(subset=["latitude", "longitude"])
    dropped = before - len(result)
    if dropped:
        print(f"  경고: 위도/경도 누락으로 {dropped}건 제외됨")

    return result


def main():
    # TODO: 새 데이터셋(어린이집, 병원 등)이 늘어나면 이 리스트에 처리 결과를 추가한다.
    cctv_raw_path = RAW_DIR / "부산_방범용_CCTV_전체.csv"
    if not cctv_raw_path.exists():
        print(f"원본 파일 없음: {cctv_raw_path} (data.go.kr에서 다운로드 후 data/raw/에 저장)")
        return

    # 원본은 부산시 전체 데이터라 '구군' 컬럼으로 사상구만 필터링
    cctv_df = pd.read_csv(cctv_raw_path, encoding="cp949")
    cctv_df = cctv_df[cctv_df["구군"] == "사상구"]

    cctv_std = standardize(
        cctv_df,
        category="안전",
        facility_type="cctv",
        source="부산광역시_방범용 CCTV 정보_20251229",
        name_col="시설명칭",
    )

    combined = pd.concat([cctv_std], ignore_index=True)

    PROCESSED_DIR.mkdir(exist_ok=True)
    out_path = PROCESSED_DIR / "facilities.csv"
    combined.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"완료: {len(combined)}건 저장됨 -> {out_path}")


if __name__ == "__main__":
    main()
