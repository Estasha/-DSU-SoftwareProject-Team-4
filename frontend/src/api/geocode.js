// 백엔드 지오코딩 API 호출 (주소/장소명 -> 좌표, 지도 이동용)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchGeocode(query) {
  const url = `${API_BASE_URL}/api/geocode?query=${encodeURIComponent(query)}`;
  const res = await fetch(url);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "좌표를 찾지 못했습니다.");
  }
  return res.json();
}
