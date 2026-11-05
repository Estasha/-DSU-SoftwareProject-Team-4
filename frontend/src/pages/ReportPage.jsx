import { useState } from "react";
import SearchBar from "../components/SearchBar.jsx";
import { fetchGeocode } from "../api/geocode.js";

// 점수 계산(fetchScore/api/score.js)은 지역 데이터가 아직 없어서 당분간 비활성화.
// 주소 검색은 지도 이동(지오코딩)까지만 수행한다.
// 지오코딩은 네이버 geocoder 대신 백엔드(카카오 주소+장소명 검색)를 쓴다 — 장소명도 인식됨.
export default function ReportPage({ onLocate } = {}) {
  const [error, setError] = useState(null);

  async function handleSearch(address) {
    setError(null);
    try {
      const point = await fetchGeocode(address);
      if (onLocate) onLocate(point);
    } catch (e) {
      setError(e.message);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">동네 진단</h1>
      <SearchBar onSearch={handleSearch} />

      {error && <p className="text-red-600">{error}</p>}
    </div>
  );
}
