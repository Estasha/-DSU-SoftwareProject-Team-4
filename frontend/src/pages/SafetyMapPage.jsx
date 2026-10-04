import { useEffect, useRef, useState } from "react";
import { fetchNearbyFacilities } from "../api/facilities.js";

const NAVER_CLIENT_ID = import.meta.env.VITE_NAVER_CLIENT_ID;
const SASANG_CENTER = { lat: 35.1524, lng: 128.9905 }; // 부산 사상구청 부근
const RADIUS_M = 100;

const LAYERS = [
  { key: "safety", label: "안전 (CCTV)", category: "안전", color: "#dc2626" },
  { key: "life", label: "생활편의", category: "생활편의", color: "#16a34a" },
  { key: "food", label: "음식점", category: "음식점", color: "#f59e0b" },
];

function loadNaverSdk() {
  return new Promise((resolve, reject) => {
    if (window.naver && window.naver.maps) {
      resolve(window.naver);
      return;
    }
    const script = document.createElement("script");
    script.src = `https://oapi.map.naver.com/openapi/v3/maps.js?ncpKeyId=${NAVER_CLIENT_ID}`;
    script.onload = () => resolve(window.naver);
    script.onerror = () => reject(new Error("네이버 지도 SDK 로드 실패"));
    document.head.appendChild(script);
  });
}

function makeDotIcon(naver, color) {
  return {
    content: `<div style="width:14px;height:14px;border-radius:50%;background:${color};border:2px solid white;box-shadow:0 0 2px rgba(0,0,0,0.5);"></div>`,
    anchor: new naver.maps.Point(7, 7),
  };
}

export default function SafetyMapPage() {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const naverRef = useRef(null);
  const overlaysRef = useRef([]);
  const lastClickRef = useRef(null);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [layerKey, setLayerKey] = useState("safety");
  const layerKeyRef = useRef(layerKey);

  const layer = LAYERS.find((l) => l.key === layerKey);

  // 지도 클릭 리스너는 처음 한 번만 등록되기 때문에, 그 안에서 state를 직접 읽으면
  // 마운트 시점의 값에 고정돼버림(stale closure) — 그래서 ref로 최신 레이어를 추적함
  useEffect(() => {
    layerKeyRef.current = layerKey;
  }, [layerKey]);

  async function searchAt(lat, lng) {
    const naver = naverRef.current;
    const map = mapRef.current;
    if (!naver || !map) return;

    const layer = LAYERS.find((l) => l.key === layerKeyRef.current);

    overlaysRef.current.forEach((overlay) => overlay.setMap(null));
    overlaysRef.current = [];

    const position = new naver.maps.LatLng(lat, lng);

    const marker = new naver.maps.Marker({ position, map });

    const circle = new naver.maps.Circle({
      map,
      center: position,
      radius: RADIUS_M,
      strokeWeight: 2,
      strokeColor: "#2563eb",
      strokeOpacity: 0.8,
      fillColor: "#3b82f6",
      fillOpacity: 0.2,
    });

    overlaysRef.current = [marker, circle];

    setResult({ lat, lng, loading: true });
    try {
      const data = await fetchNearbyFacilities(lat, lng, RADIUS_M, { category: layer.category });

      const facilityMarkers = data.facilities.map((f) => {
        const fMarker = new naver.maps.Marker({
          position: new naver.maps.LatLng(f.latitude, f.longitude),
          map,
          icon: makeDotIcon(naver, layer.color),
          title: f.name || layer.label,
          zIndex: 50,
        });

        const infoWindow = new naver.maps.InfoWindow({
          content: `<div style="padding:6px 10px;font-size:12px;">${f.name || layer.label}<br/>${f.distance_m}m</div>`,
        });
        naver.maps.Event.addListener(fMarker, "click", () => {
          infoWindow.open(map, fMarker);
        });

        return fMarker;
      });

      overlaysRef.current = [...overlaysRef.current, ...facilityMarkers];

      setResult({ lat, lng, count: data.count, facilities: data.facilities });
    } catch (e) {
      setError(e.message);
      setResult(null);
    }
  }

  useEffect(() => {
    if (!NAVER_CLIENT_ID) {
      setError("VITE_NAVER_CLIENT_ID가 설정되지 않았습니다. frontend/.env에 키를 넣어주세요.");
      return;
    }

    let cancelled = false;

    loadNaverSdk()
      .then((naver) => {
        if (cancelled || !mapContainerRef.current) return;
        naverRef.current = naver;

        const map = new naver.maps.Map(mapContainerRef.current, {
          center: new naver.maps.LatLng(SASANG_CENTER.lat, SASANG_CENTER.lng),
          zoom: 15,
        });
        mapRef.current = map;

        naver.maps.Event.addListener(map, "click", (pointerEvent) => {
          const lat = pointerEvent.coord.lat();
          const lng = pointerEvent.coord.lng();
          lastClickRef.current = { lat, lng };
          searchAt(lat, lng);
        });
      })
      .catch((e) => setError(e.message));

    return () => {
      cancelled = true;
    };
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  // 레이어를 바꾸면, 이미 클릭했던 지점 기준으로 다시 조회
  useEffect(() => {
    if (lastClickRef.current) {
      searchAt(lastClickRef.current.lat, lastClickRef.current.lng);
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [layerKey]);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold">동네 편의·방범 지도 (사상구, 부산)</h1>
      <p className="text-sm text-gray-500">
        항목을 고르고 지도를 클릭하면 그 지점 반경 {RADIUS_M}m 안의 위치(점)와 개수를 보여줍니다. 점을 클릭하면 이름이 뜹니다.
      </p>

      <div className="flex gap-2">
        {LAYERS.map((l) => (
          <button
            key={l.key}
            onClick={() => setLayerKey(l.key)}
            className={`px-3 py-1.5 rounded-lg text-sm border ${
              layerKey === l.key ? "text-white" : "bg-gray-100"
            }`}
            style={layerKey === l.key ? { backgroundColor: l.color, borderColor: l.color } : {}}
          >
            {l.label}
          </button>
        ))}
      </div>

      {error && <p className="text-red-600">{error}</p>}

      <div ref={mapContainerRef} className="w-full h-[420px] rounded-lg border" />

      {result && (
        <div className="p-4 rounded-lg shadow bg-white space-y-2">
          <p className="text-sm text-gray-500">
            클릭 좌표: {result.lat.toFixed(5)}, {result.lng.toFixed(5)}
          </p>
          <p className="text-lg font-semibold">
            반경 {RADIUS_M}m 내 {layer.label}: {result.loading ? "조회 중..." : `${result.count}개`}
          </p>

          {result.facilities && result.facilities.length > 0 && (
            <ul className="text-sm text-gray-700 divide-y max-h-64 overflow-y-auto">
              {result.facilities.map((f, i) => (
                <li key={i} className="py-1 flex justify-between gap-2">
                  <span className="truncate">{f.name || layer.label}</span>
                  <span className="text-gray-400 shrink-0">{f.distance_m}m</span>
                </li>
              ))}
            </ul>
          )}
        </div>
      )}
    </div>
  );
}
