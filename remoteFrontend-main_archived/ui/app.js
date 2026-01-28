const express = require("express");
const mysql = require("mysql2");
const path = require("path");

const app = express();
const port = 3000;

// MySQL connection
const db = mysql.createConnection({
  //host: "localhost";
  host: "host.docker.internal",
  port: 3306,
  user: "root",
  password: "root",
  database: "Test",
});

db.connect((err) => {
  if (err) {
    console.error("\x1b[31m [Database] \x1b[37m Database connection failed:", err);
  } else {
    console.log("\x1b[32m [Database] \x1b[37m Connected to MySQL database 'Test'");
  }
});

app.use(express.static(path.join(__dirname, "public")));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, "public", "index.html"));
});


app.get('/graph', (req, res) => {
  res.sendFile(path.join(__dirname, "public", "graphs.html"));
});

app.get("/test", (req, res) => {
  res.send("Server is alive!");
});


// API endpoint to get power data
app.get("/api/power", (req, res) => {
  const query = "SELECT timestamp_data, power_value FROM Power ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("\x1b[31m [Database] \x1b[37m Error fetching power data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get voltage data
app.get("/api/volt", (req, res) => {
  const query = "SELECT timestamp_data, volt_value FROM Voltage ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("\x1b[31m [Database] \x1b[37m Error fetching volt data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

app.listen(port, () => {
  console.log(`\x1b[36m [Project56 Remote UI] \x1b[37m UI Running on port ${port}`);
});
