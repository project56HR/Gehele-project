window.addEventListener("load", () => {
    const wsEndpoints = {
        volt: "ws://100.79.129.74:32848/volt",
        watt:  "ws://100.79.129.74:32848/watt"
    };

    const wsConnections = {};

    for (const [key, url] of Object.entries(wsEndpoints)) {
        const ws = new WebSocket(url);
        wsConnections[key] = ws;

        ws.onopen = () => {
            console.log(`[WebSocket] Connected to ${url}`);
        };

        ws.onmessage = (event) => {
            console.log(`[WebSocket] Received on ${key}:`, event.data);

            switch (key) {
                case "volt":
                    document.getElementById("electrical-voltage").textContent = event.data;
                    document.getElementById("battery1-voltage").textContent = event.data;
                    break;
                case "watt":
                    const watts = parseFloat(event.data);

                    document.getElementById("battery1-powerin").textContent = watts.toFixed(2);
                    document.getElementById("electrical-powerin").textContent = event.data;


                    const windspeed = calculateWindSpeedFromPower(watts);
                    document.getElementById("wingenerator-speed").textContent = windspeed.toFixed(2) + " m/s";

                    break;

            }
        };

        ws.onerror = (err) => {
            console.error(`[WebSocket] Error on ${key}:`, err.message || err);
        };

        ws.onclose = () => {
            console.log(`[WebSocket] Connection closed on ${key}`);
        };
    }
});

function calculateWindSpeedFromPower(p) {
    /*
      Calculates wind speed (m/s) required to generate a specific power (W)
      Inverted formula:
      P = 0.208 * (v^3 - 3.5^3)
      v = cube_root((P / 0.208) + 3.5^3)
    */

    if (p <= 0) {
        return 0.0;
    }

    if (p >= 350) {
        console.log("Note: At 350W, wind speed is >= 12.0 m/s (turbine is regulating).");
        p = 350;
    }

    return Math.cbrt((p / 0.208) + Math.pow(3.5, 3));
}

