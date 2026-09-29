import { useEffect, useRef, useState } from "react";
import { fetchNearbyFacilities } from "../api/facilities.js";

const NAVER_CLIENT_ID = import.meta.env.VITE_NAVER_CLIENT_ID;
const SASANG_CENTER = { lat: 35.1524, lng: 128.9905 }; // 부산 사상구청 부근
const RADIUS_M = 100;

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

export default function SafetyMapPage() {
  const mapContainerRef = useRef(null);
  const mapRef = useRef(null);
  const overlaysRef = useRef([]);
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);

  useEffect(() => {
    if (!NAVER_CLIENT_ID) {
      setError("VITE_NAVER_CLIENT_ID가 설정되지 않았습니다. frontend/.env에 키를 넣어주세요.");
      return;
    }

    let cancelled = false;

    loadNaverSdk()
      .then((naver) => {
        if (cancelled || !mapContainerRef.current) return;

        const map = new naver.maps.Map(mapContainerRef.current, {
          center: new naver.maps.LatLng(SASANG_CENTER.lat, SASANG_CENTER.lng),
          zoom: 15,
        });
        mapRef.current = map;

        naver.maps.Event.addListener(map, "click", async (pointerEvent) => {
          const lat = pointerEvent.coord.lat();
          const lng = pointerEvent.coord.lng();

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
            const data = await fetchNearbyFacilities(lat, lng, RADIUS_M, "cctv");
            setResult({ lat, lng, cctvCount: data.count });
          } catch (e) {
            setError(e.message);
            setResult(null);
          }
        });
      })
      .catch((e) => setError(e.message));

    return () => {
      cancelled = true;
    };
  }, []);

  return (
    <div className="max-w-3xl mx-auto p-6 space-y-4">
      <h1 className="text-2xl font-bold">동네 방범지도 (사상구, 부산)</h1>
      <p className="text-sm text-gray-500">
        지도를 클릭하면 그 지점 반경 {RADIUS_M}m 안의 실제 CCTV 개수를 보여줍니다.
      </p>

      {error && <p className="text-red-600">{error}</p>}

      <div ref={mapContainerRef} className="w-full h-[420px] rounded-lg border" />

      {result && (
        <div className="p-4 rounded-lg shadow bg-white space-y-1">
          <p className="text-sm text-gray-500">
            클릭 좌표: {result.lat.toFixed(5)}, {result.lng.toFixed(5)}
          </p>
          <p className="text-lg font-semibold">
            반경 {RADIUS_M}m 내 CCTV: {result.loading ? "조회 중..." : `${result.cctvCount}개`}
          </p>
        </div>
      )}
    </div>
  );
}
