// 백엔드 API 호출 함수 모음
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export async function fetchScore(address) {
  const url = `${API_BASE_URL}/api/score?address=${encodeURIComponent(address)}`;
  const res = await fetch(url);
  if (!res.ok) {
    const err = await res.json().catch(() => ({}));
    throw new Error(err.detail || "점수를 불러오지 못했습니다.");
  }
  return res.json();
}
