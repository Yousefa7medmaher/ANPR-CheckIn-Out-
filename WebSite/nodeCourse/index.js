const express = require("express");
const mysql = require("mysql2");
const cors = require("cors");
const methodOverride = require("method-override");

const app = express();
const PORT = 3000;

// Middleware
app.use(cors());
app.use(express.json());
app.set("view engine", "ejs"); // Set EJS as the view engine
app.use(express.static("public")); // Serve static files
app.use(methodOverride("_method")); // Override POST to DELETE method

// MySQL Connection
const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "1234",
  database: "car_log_db"
});

// Connect to database
db.connect((err) => {
  if (err) {
    console.error("Database connection failed: " + err.stack);
    return;
  }
  console.log("Connected to MySQL database");
});

// Fetch car logs and render to EJS
app.get("/", (req, res) => {
  const sql = "SELECT * FROM car_log";
  db.query(sql, (err, results) => {
    if (err) {
      return res.status(500).send("Database error: " + err.message);
    }
    res.render("index", { cars: results });
  });
});

// API to return car data as JSON
app.get("/cars", (req, res) => {
  const sql = "SELECT * FROM car_log";
  db.query(sql, (err, results) => {
    if (err) {
      return res.status(500).json({ error: err.message });
    }
    res.json(results);
  });
});

// DELETE a car log entry by ID
app.delete("/delete/:id", (req, res) => {
  const { id } = req.params;
  const sql = "DELETE FROM car_log WHERE id = ?";

  db.query(sql, [id], (err, result) => {
    if (err) {
      return res.status(500).json({ error: "Database error: " + err.message });
    }
    res.redirect("/"); // Redirect back to the index page after deletion
  });
});

// Start server
app.listen(PORT, () => {
  console.log(`Server is running on http://localhost:${PORT}`);
});
