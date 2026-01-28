window.addEventListener("load", () => {
    const wsEndpoints = {
        volt: "ws://raspberrypi.local:32848/volt",
        amp:  "ws://raspberrypi.local:32848/amp",
        soc:  "ws://raspberrypi.local:32848/soc"
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
                case "amp":
                    document.getElementById("electrical-powerin").textContent = event.data;
                    document.getElementById("battery1-powerin").textContent = event.data;
                    break;
                case "soc":
                    document.getElementById("wingenerator-speed").textContent = event.data;
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
