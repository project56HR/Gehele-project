const URL_WEB_SOCKET = 'ws://192.168.2.58:32848/';
const ws_watt = new WebSocket("ws://192.168.2.58:32848/watt");
const ws_rpm = new WebSocket("ws://192.168.2.58:32848/RPM");
const ws_soc = new WebSocket("ws://192.168.2.58:32848/SoC");

ws_watt.onopen = () => {
  console.log(`[WebSocket/watt] Connected to ${URL_WEB_SOCKET}`);
};

ws_watt.onmessage = (event) => {
  console.log('[WebSocket/watt] Received:', event.data);
  document.getElementById("electrical-powerin").textContent = event.data;
};

ws_watt.onerror = (err) => {
  console.error('[WebSocket/watt] Error:', err.message);
};

ws_watt.onclose = () => {
  console.log('[WebSocket/watt] Connection closed');
};


ws_rpm.onopen = () => {
  console.log(`[WebSocket/rpm] Connected to ${URL_WEB_SOCKET}`);
};

ws_rpm.onmessage = (event) => {
  console.log('[WebSocket/rpm] Received:', event.data);
  document.getElementById("windgenerator-rpm").textContent = event.data;
};

ws_rpm.onerror = (err) => {
  console.error('[WebSocket/rpm] Error:', err.message);
};

ws_rpm.onclose = () => {
  console.log('[WebSocket/rpm] Connection closed');
};
