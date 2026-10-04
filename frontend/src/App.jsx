import { useState } from "react";
import ReportPage from "./pages/ReportPage.jsx";
import SafetyMapPage from "./pages/SafetyMapPage.jsx";

export default function App() {
  const [tab, setTab] = useState("report");

  return (
    <div>
      <nav className="flex gap-2 justify-center p-4 border-b">
        <button
          onClick={() => setTab("report")}
          className={`px-4 py-2 rounded-lg ${tab === "report" ? "bg-blue-600 text-white" : "bg-gray-100"}`}
        >
          점수 리포트
        </button>
        <button
          onClick={() => setTab("map")}
          className={`px-4 py-2 rounded-lg ${tab === "map" ? "bg-blue-600 text-white" : "bg-gray-100"}`}
        >
          동네 지도 (테스트)
        </button>
      </nav>

      {tab === "report" ? <ReportPage /> : <SafetyMapPage />}
    </div>
  );
}
