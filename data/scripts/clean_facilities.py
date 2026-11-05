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


# 상가업소정보의 업종대분류명(indsLclsNm) -> 우리 스키마 매핑.
# 매핑에 없는 대분류(수리·개인, 과학·기술, 교육, 부동산, 시설관리·임대, 숙박)는 제외.
STORE_CATEGORY_MAP = {
    "소매": ("생활편의", "소매"),
    "보건의료": ("생활편의", "보건의료"),
    "예술·스포츠": ("생활편의", "문화체육"),
    "음식": ("음식점", "음식점"),  # 생활편의 점수엔 기본 미포함, 별도 카테고리로 분리
}


def standardize_stores(df: pd.DataFrame, source: str) -> pd.DataFrame:
    """상가업소정보는 indsLclsNm 값에 따라 category/facility_type이 달라져서 별도 처리."""
    rows = []
    for _, row in df.iterrows():
        mapping = STORE_CATEGORY_MAP.get(row["indsLclsNm"])
        if not mapping:
            continue
        category, facility_type = mapping
        rows.append({
            "category": category,
            "facility_type": facility_type,
            "name": row["bizesNm"],
            "latitude": row["lat"],
            "longitude": row["lon"],
            "source": source,
        })

    result = pd.DataFrame(rows)
    result["latitude"] = pd.to_numeric(result["latitude"], errors="coerce")
    result["longitude"] = pd.to_numeric(result["longitude"], errors="coerce")

    before = len(result)
    result = result.dropna(subset=["latitude", "longitude"])
    dropped = before - len(result)
    if dropped:
        print(f"  경고: 위도/경도 누락으로 {dropped}건 제외됨")

    return result


def main():
    cctv_raw_path = RAW_DIR / "부산_방범용_CCTV_전체.csv"
    stores_raw_path = RAW_DIR / "사상구_상가업소정보.csv"
    subway_raw_path = RAW_DIR / "부산_도시철도역사정보.csv"
    bus_processed_path = PROCESSED_DIR / "사상구_버스정류소.csv"

    combined_parts = []

    if cctv_raw_path.exists():
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
        combined_parts.append(cctv_std)
        print(f"CCTV: {len(cctv_std)}건")
    else:
        print(f"원본 파일 없음: {cctv_raw_path} (건너뜀)")

    if stores_raw_path.exists():
        stores_df = pd.read_csv(stores_raw_path, encoding="utf-8-sig")
        stores_std = standardize_stores(
            stores_df,
            source="소상공인시장진흥공단_상가업소정보",
        )
        combined_parts.append(stores_std)
        print(f"상가업소: {len(stores_std)}건 (업종 필터링 후)")
    else:
        print(f"원본 파일 없음: {stores_raw_path} (건너뜀, fetch_stores.py 먼저 실행)")

    if subway_raw_path.exists():
        # 공공데이터포털 다운로드 파일이 UTF-16 탭구분(TSV)으로 내려옴
        subway_df = pd.read_csv(subway_raw_path, encoding="utf-16", sep="\t")
        # 원본은 부산 전체 노선 데이터라 주소에 '사상구'가 들어간 역만 필터링
        subway_df = subway_df[subway_df["역사도로명주소"].str.contains("사상구", na=False)]
        subway_std = standardize(
            subway_df,
            category="교통",
            facility_type="지하철역",
            source="부산교통공사_도시철도역사정보_20210226",
            name_col="역사명",
            lat_col="역위도",
            lng_col="역경도",
        )
        combined_parts.append(subway_std)
        print(f"지하철역: {len(subway_std)}건")
    else:
        print(f"원본 파일 없음: {subway_raw_path} (건너뜀)")

    if bus_processed_path.exists():
        # 팀원이 TAGO API + 사상구 행정동 경계 폴리곤으로 이미 정확하게 필터링해둔 결과
        # (data/scripts/collect_busstop_api.py 참고 — citycode는 행정구역과 안 맞아서
        # point-in-polygon 판정으로 거름)
        bus_df = pd.read_csv(bus_processed_path, encoding="utf-8-sig")
        bus_std = standardize(
            bus_df,
            category="교통",
            facility_type="버스정류장",
            source="국가대중교통정보센터(TAGO)_버스정류소정보",
            name_col="정류소명",
            lat_col="위도",
            lng_col="경도",
        )
        combined_parts.append(bus_std)
        print(f"버스정류장: {len(bus_std)}건 (사상구 행정동 경계 기준)")
    else:
        print(f"원본 파일 없음: {bus_processed_path} (건너뜀)")

    if not combined_parts:
        print("처리할 데이터가 없습니다.")
        return

    combined = pd.concat(combined_parts, ignore_index=True)

    PROCESSED_DIR.mkdir(exist_ok=True)
    out_path = PROCESSED_DIR / "facilities.csv"
    combined.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"완료: {len(combined)}건 저장됨 -> {out_path}")


if __name__ == "__main__":
    main()
