import { useState } from "react";
import {
  getRadiusLimit,
  setRadiusLimit,
  RADIUS_MIN,
  RADIUS_MAX,
  RADIUS_STEP,
} from "../lib/settings.js";

export default function AdminPage() {
  const [limit, setLimit] = useState(() => getRadiusLimit());
  const [saved, setSaved] = useState(false);

  function handleChange(e) {
    const value = Number(e.target.value);
    setLimit(value);
    setRadiusLimit(value);
    setSaved(true);
  }

  return (
    <div className="max-w-2xl mx-auto p-6 space-y-6">
      <h1 className="text-2xl font-bold">관리자 메뉴</h1>

      <div className="p-4 rounded-lg border space-y-3">
        <h2 className="font-semibold">검색 범위 허용 최대값 설정 (FR-10)</h2>
        <p className="text-sm text-gray-500">
          메인 화면에서 사용자가 조절할 수 있는 검색 범위의 최대값입니다. 예를 들어 500m로 설정하면
          사용자는 지도에서 50m~500m 사이에서 반경을 직접 고를 수 있습니다. 설정한 값은 다음에
          메인 화면을 열 때부터 적용됩니다.
        </p>
        <input
          type="range"
          min={RADIUS_MIN}
          max={RADIUS_MAX}
          step={RADIUS_STEP}
          value={limit}
          onChange={handleChange}
          className="w-full"
        />
        <div className="flex justify-between text-xs text-gray-400">
          <span>{RADIUS_MIN}m</span>
          <span className="text-base font-semibold text-gray-800">최대 {limit}m</span>
          <span>{RADIUS_MAX}m</span>
        </div>
        {saved && <p className="text-sm text-green-600">저장됨</p>}
      </div>

      <p className="text-sm text-gray-500">
        데이터 즉시 최신화(FR-09) 기능이 이후 이 화면에 추가됩니다.
      </p>
    </div>
  );
}
