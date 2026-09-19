import { useState } from "react";
import SearchBar from "../components/SearchBar.jsx";
import ScoreCard from "../components/ScoreCard.jsx";
import { fetchScore } from "../api/score.js";

export default function ReportPage() {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  async function handleSearch(address) {
    setError(null);
    try {
      const result = await fetchScore(address);
      setData(result);
    } catch (e) {
      setError(e.message);
      setData(null);
    }
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">동네 진단</h1>
      <SearchBar onSearch={handleSearch} />

      {error && <p className="text-red-600">{error}</p>}

      {data && (
        <div className="space-y-4">
          <h2 className="text-lg font-semibold">{data.region} 종합 점수: {data.final_score}점</h2>
          <div className="grid grid-cols-3 gap-4">
            <ScoreCard title="안전" score={data.safety_score} />
            <ScoreCard title="생활편의" score={data.facility_score} />
            <ScoreCard title="교통" score={data.transit_score} />
          </div>
        </div>
      )}
    </div>
  );
}
