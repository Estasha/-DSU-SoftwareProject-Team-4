// 백엔드 시설(CCTV 등) 조회 API 호출 함수 모음
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchNearbyFacilities(lat, lng, radiusM = 100, { facilityType, category } = {}) {
  const params = new URLSearchParams({ lat, lng, radius_m: radiusM });
  if (facilityType) params.set("facility_type", facilityType);
  if (category) params.set("category", category);

  const res = await fetch(`${API_BASE_URL}/api/facilities/nearby?${params}`);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "주변 시설 정보를 불러오지 못했습니다.");
  }
  return res.json();
}
