// 네이버 지도 JS SDK를 한 번만 로드해서 지도 컴포넌트가 쓴다.
export const NAVER_CLIENT_ID = import.meta.env.VITE_NAVER_CLIENT_ID;

let loadPromise = null;

export function loadNaverSdk() {
  if (!NAVER_CLIENT_ID) {
    return Promise.reject(new Error("VITE_NAVER_CLIENT_ID가 설정되지 않았습니다. frontend/.env에 키를 넣어주세요."));
  }
  if (!loadPromise) {
    loadPromise = new Promise((resolve, reject) => {
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
  return loadPromise;
}
