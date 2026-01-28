// app.js
const express = require("express");
const app = express();
const port = 3000;

// ✅ Route for testing
app.get("/test", (req, res) => {
    res.send("Server is alive!");
});

// ✅ Start server
app.listen(port, () => {
    console.log(`🚀 Server running at http://localhost:${port}`);
    console.log("Running from file:", __filename);
    process.on("uncaughtException", err => console.error("🔥 Uncaught exception:", err));
    process.on("unhandledRejection", err => console.error("💥 Unhandled promise rejection:", err));

});

