"""점수 계산 가중치 초기값을 DB에 심는 일회성 스크립트.

docs/동네 진단 서비스 정주여건 점수 계산 방식.md 의 '파라미터 초안' 표 그대로를 넣는다.
페르소나(개인/가족/노인)별 가중치는 아직 AHP 설문 결과가 없어서, 일단 세 페르소나 모두
같은 초안 값으로 심어둔다 — 나중에 결과가 나오면 관리자 페이지나 API로 페르소나별로
다르게 고치면 된다.
이미 값이 있으면 아무것도 하지 않는다(여러 번 실행해도 안전).

실행: python -m app.seed_weights
"""
from .db import Base, engine, SessionLocal
from .models import CategoryParam, PersonaCategoryWeight, PersonaFacilityTypeWeight

PERSONAS = ["개인", "가족", "노인"]

CATEGORY_PARAMS = [
    # score_category, radius_m(r_c), target_count(n_c)
    ("안전", 300, 4),
    ("의료_의원급", 500, 2),
    # 종합병원은 반경 안 개수가 아니라 최근접 거리로 계산하므로, radius_m은
    # "이 거리 안에서 가장 가까운 종합병원을 찾는다"는 검색 반경으로 씀. target_count는 미사용
    ("의료_종합병원", 5000, 0),
    ("생필품", 400, 3),
    ("버스", 400, 2),
    ("지하철", 800, 1),
]

# 페르소나별 카테고리 가중치(W_c). '의료_의원급'은 종합병원과 합산한 '의료' 전체 가중치를 뜻함.
# 아직 AHP 결과가 없어 세 페르소나 모두 문서의 초안 값과 동일 (합계 1.0)
CATEGORY_WEIGHTS = {
    "안전": 0.20,
    "의료_의원급": 0.25,
    "의료_종합병원": 0.0,
    "생필품": 0.20,
    "버스": 0.15,
    "지하철": 0.20,
}

FACILITY_TYPE_WEIGHTS = [
    # facility_type, score_category, weight(wᵢ)
    ("cctv", "안전", 1.0),
    ("내과/소아과 의원", "의료_의원급", 0.6),
    ("피부/비뇨기과 의원", "의료_의원급", 0.1),
    ("성형외과 의원", "의료_의원급", 0.1),
    ("종합병원", "의료_종합병원", 1.0),
    ("슈퍼마켓", "생필품", 1.0),
    ("편의점", "생필품", 1.0),
    ("약국", "생필품", 1.0),
    ("버스정류장", "버스", 1.0),
    ("지하철역", "지하철", 1.0),
]


def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        if db.query(CategoryParam).count() == 0:
            for score_category, r_c, n_c in CATEGORY_PARAMS:
                db.add(CategoryParam(score_category=score_category, radius_m=r_c, target_count=n_c))
            print(f"CategoryParam {len(CATEGORY_PARAMS)}건 추가")
        else:
            print("CategoryParam 이미 데이터 있음, 건너뜀")

        if db.query(PersonaCategoryWeight).count() == 0:
            count = 0
            for persona in PERSONAS:
                for score_category, w_c in CATEGORY_WEIGHTS.items():
                    db.add(PersonaCategoryWeight(persona=persona, score_category=score_category, category_weight=w_c))
                    count += 1
            print(f"PersonaCategoryWeight {count}건 추가 ({len(PERSONAS)}개 페르소나 x {len(CATEGORY_WEIGHTS)}개 카테고리)")
        else:
            print("PersonaCategoryWeight 이미 데이터 있음, 건너뜀")

        if db.query(PersonaFacilityTypeWeight).count() == 0:
            count = 0
            for persona in PERSONAS:
                for facility_type, score_category, weight in FACILITY_TYPE_WEIGHTS:
                    db.add(
                        PersonaFacilityTypeWeight(
                            persona=persona,
                            facility_type=facility_type,
                            score_category=score_category,
                            weight=weight,
                        )
                    )
                    count += 1
            print(f"PersonaFacilityTypeWeight {count}건 추가 ({len(PERSONAS)}개 페르소나 x {len(FACILITY_TYPE_WEIGHTS)}개 유형)")
        else:
            print("PersonaFacilityTypeWeight 이미 데이터 있음, 건너뜀")

        db.commit()
    finally:
        db.close()


if __name__ == "__main__":
    main()
