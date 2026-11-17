// FR-10: 검색 범위 허용 최대값 설정 — 관리자가 정하는 값은 메인 화면에서 사용자가 직접
// 고를 수 있는 검색 범위의 "상한"이다. 예: 관리자가 500m로 정하면, 사용자는 메인 화면에서
// 50m~500m 사이에서 원하는 반경을 고를 수 있다.
const RADIUS_LIMIT_KEY = "dongneJindan.radiusLimitM";

export const RADIUS_MIN = 50;
export const RADIUS_MAX = 1000;
export const RADIUS_STEP = 50;
export const RADIUS_LIMIT_DEFAULT = 100;

export function getRadiusLimit() {
  let raw = null;
  try {
    raw = localStorage.getItem(RADIUS_LIMIT_KEY);
  } catch {
    return RADIUS_LIMIT_DEFAULT;
  }
  const value = Number(raw);
  if (!raw || Number.isNaN(value) || value < RADIUS_MIN || value > RADIUS_MAX) {
    return RADIUS_LIMIT_DEFAULT;
  }
  return value;
}

export function setRadiusLimit(value) {
  try {
    localStorage.setItem(RADIUS_LIMIT_KEY, String(value));
  } catch {
    // 저장 안 되면(프라이빗 모드 등) 조용히 무시 — 이번 세션에서만 반영됨
  }
}
