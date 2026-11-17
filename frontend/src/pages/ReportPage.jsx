import { useState } from "react";
import SearchBar from "../components/SearchBar.jsx";
import { fetchGeocode } from "../api/geocode.js";
import { PERSONAS } from "../api/weights.js";

// 주소 검색 + 페르소나 선택만 담당. 점수·시설 결과는 SafetyMapPage에서 지도와 함께 한 번에 보여준다.
export default function ReportPage({ persona, onPersonaChange, onLocate } = {}) {
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);

  async function handleSearch(address) {
    setError(null);
    setLoading(true);
    try {
      const point = await fetchGeocode(address);
      if (onLocate) onLocate(point);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-4">
      <h1 className="text-2xl font-bold">동네 진단</h1>

      <div className="flex gap-2">
        {PERSONAS.map((p) => (
          <button
            key={p}
            onClick={() => onPersonaChange?.(p)}
            className={`px-3 py-1.5 rounded-lg text-sm ${
              persona === p ? "bg-blue-600 text-white" : "bg-gray-100"
            }`}
          >
            {p}
          </button>
        ))}
      </div>

      <SearchBar onSearch={handleSearch} />

      {loading && <p className="text-sm text-gray-500">위치 찾는 중...</p>}
      {error && <p className="text-red-600">{error}</p>}

      <p className="text-sm text-gray-500">
        주소를 검색하거나 오른쪽 지도를 클릭하면, 그 지점의 점수와 주변 시설이 함께 표시됩니다.
      </p>
    </div>
  );
}
