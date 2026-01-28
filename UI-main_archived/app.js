const express = require("express");
const mysql = require("mysql2");
const path = require("path");
import proxy from "express-http-proxy";

const app = express();
const port = 3000;

// MySQL connection
const db = mysql.createConnection({
  //host: "localhost";
  host: "host.docker.internal",   // or your DB container name in Docker
  port: 3306,
  user: "root",
  password: "root",
  database: "Dummydata",
});

db.connect((err) => {
  if (err) {
    console.error("❌ Database connection failed:", err);
  } else {
    console.log("✅ Connected to MySQL database 'Dummydata'");
  }
});

// db.query("SELECT * FROM Power", (err, results) => {
//   if (err) {
//     console.error("❌ Error querying database:", err);
//   } else {
//     console.log("✅ Data from Power table:", results);
//   }
// });

// db.query("SELECT * FROM Voltage", (err, results) => {
//   if (err) {
//     console.error("❌ Error querying database:", err);
//   } else {
//     console.log("✅ Data from Power table:", results);
//   }
// });

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


// API endpoint to get power data
app.get("/api/power", (req, res) => {
  const query = "SELECT timestamp_data, power_value FROM Power ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching power data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get weekly power data
app.get("/api/power/week", (req, res) => {
  const query = "SELECT timestamp_data, powerW_value FROM PowerWeek ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching weekly power data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get monthly power data
app.get("/api/power/month", (req, res) => {
  const query = "SELECT timestamp_data, powerM_value FROM PowerMonth ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching monthly power data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get yearly power data
app.get("/api/power/year", (req, res) => {
  const query = "SELECT timestamp_data, powerY_value FROM PowerYear ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching yearly power data:", err);
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
      console.error("Error fetching volt data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get weekly power data
app.get("/api/volt/week", (req, res) => {
  const query = "SELECT timestamp_data, voltW_value FROM VoltWeek ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching weekly volt data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get monthly power data
app.get("/api/volt/month", (req, res) => {
  const query = "SELECT timestamp_data, voltM_value FROM VoltMonth ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching monthly volt data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

// API endpoint to get yearly power data
app.get("/api/volt/year", (req, res) => {
  const query = "SELECT timestamp_data, voltY_value FROM VoltYear ORDER BY timestamp_data ASC";
  db.query(query, (err, results) => {
    if (err) {
      console.error("Error fetching yearly volt data:", err);
      res.status(500).json({ error: "Database query failed" });
    } else {
      res.json(results);
    }
  });
});

app.listen(port, () => {
  console.log(`[Project56 Remote UI] UI Running on port ${port}`);
});
