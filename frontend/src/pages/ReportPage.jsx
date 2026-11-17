import { useState } from "react";
import SearchBar from "../components/SearchBar.jsx";
import { fetchGeocode } from "../api/geocode.js";
import { fetchScore } from "../api/score.js";
import { PERSONAS } from "../api/weights.js";

const CATEGORY_LABELS = {
  안전: "안전",
  의료_의원급: "의료(의원)",
  의료_종합병원: "의료(종합병원)",
  생필품: "생필품",
  버스: "버스",
  지하철: "지하철",
};

export default function ReportPage({ onLocate } = {}) {
  const [persona, setPersona] = useState(PERSONAS[0]);
  const [error, setError] = useState(null);
  const [loading, setLoading] = useState(false);
  const [score, setScore] = useState(null);

  async function handleSearch(address) {
    setError(null);
    setScore(null);
    setLoading(true);
    try {
      // 지도 이동(지오코딩)과 점수 계산을 동시에 요청
      const [point, scoreResult] = await Promise.all([
        fetchGeocode(address),
        fetchScore(address, persona),
      ]);
      if (onLocate) onLocate(point);
      setScore(scoreResult);
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">동네 진단</h1>

      <div className="flex gap-2">
        {PERSONAS.map((p) => (
          <button
            key={p}
            onClick={() => setPersona(p)}
            className={`px-3 py-1.5 rounded-lg text-sm ${
              persona === p ? "bg-blue-600 text-white" : "bg-gray-100"
            }`}
          >
            {p}
          </button>
        ))}
      </div>

      <SearchBar onSearch={handleSearch} />

      {loading && <p className="text-sm text-gray-500">점수 계산 중...</p>}
      {error && <p className="text-red-600">{error}</p>}

      {score && (
        <div className="p-4 rounded-lg border space-y-3">
          <div className="flex items-baseline justify-between">
            <span className="text-sm text-gray-500">[{persona}] 정주여건 점수</span>
            <span className="text-3xl font-bold">{score.total_score}점</span>
          </div>

          <div className="space-y-2">
            {score.categories
              .filter((c) => c.score_category !== "의료_종합병원")
              .map((c) => (
                <div key={c.score_category} className="flex items-center gap-2">
                  <span className="w-24 text-sm text-gray-600">
                    {CATEGORY_LABELS[c.score_category] || c.score_category}
                  </span>
                  <div className="flex-1 h-2 bg-gray-100 rounded-full overflow-hidden">
                    <div
                      className="h-full bg-blue-500"
                      style={{ width: `${Math.round(c.score * 100)}%` }}
                    />
                  </div>
                  <span className="w-10 text-right text-sm text-gray-500">
                    {Math.round(c.score * 100)}
                  </span>
                </div>
              ))}
          </div>

          <div className="pt-2 border-t text-xs text-gray-500 space-y-1">
            {score.categories
              .filter((c) => c.nearby.length > 0)
              .map((c) => (
                <p key={c.score_category}>
                  {CATEGORY_LABELS[c.score_category] || c.score_category}: 반경 안{" "}
                  {c.nearby.length}곳
                  {c.nearby[0] && ` (가장 가까운 곳 ${Math.round(c.nearby[0].distance_m)}m)`}
                </p>
              ))}
          </div>
        </div>
      )}
    </div>
  );
}
