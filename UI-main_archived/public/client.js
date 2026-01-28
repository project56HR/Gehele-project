const URL_WEB_SOCKET = 'ws://localhost:32848/';
const ws_watt = new WebSocket("ws://localhost:32848/watt");
const ws_rpm = new WebSocket("ws://localhost:32848/RPM");
const ws_soc = new WebSocket("ws://localhost:32848/SoC");



ws_watt.onopen = () => {
  console.log(`[WebSocket] Connected to ${URL_WEB_SOCKET}`);
};

ws_watt.onmessage = (event) => {
  console.log('[WebSocket] Received:', event.data);
  document.getElementById("electrical-powerin").textContent = event.data;
};

ws_watt.onerror = (err) => {
  console.error('[WebSocket] Error:', err.message);
};

ws_watt.onclose = () => {
  console.log('[WebSocket] Connection closed');
};


ws_rpm.onopen = () => {
  console.log(`[WebSocket] Connected to ${URL_WEB_SOCKET}`);
};

ws_rpm.onmessage = (event) => {
  console.log('[WebSocket] Received:', event.data);
  document.getElementById("windgenerator-rpm").textContent = event.data;
};

ws_rpm.onerror = (err) => {
  console.error('[WebSocket] Error:', err.message);
};

ws_rpm.onclose = () => {
  console.log('[WebSocket] Connection closed');
};
