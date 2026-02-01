const express = require("express");
const path = require("path");
const proxy = require("express-http-proxy");
const app = express();
const port = 3000;

app.use(express.static(path.join(__dirname, "public")));

// Proxy all /api requests to FastAPI (port 8001)
app.use("/api", proxy("http://127.0.0.1:8001", {
  proxyReqPathResolver: (req) => {
    return req.originalUrl.replace(/^\/api/, "");
  },
}));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});


app.get('/graph', (req, res) => {
  res.sendFile(path.join(__dirname, "public", "graphs.html"));
});

app.get("/test", (req, res) => {
  res.send("Server is alive!");
});


app.listen(port, () => {
  console.log(`[Project56 Remote UI] UI Running on port ${port}`);
});
