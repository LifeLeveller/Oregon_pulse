const express = require("express");
const cors = require("cors");
require("dotenv").config();

const app = express();
const PORT = process.env.PORT || 3001;
const FASTAPI_URL = process.env.FASTAPI_URL || "http://localhost:8000";

app.use(cors());
app.use(express.json());

app.get("/health", (req, res) => {
  res.json({ status: "ok", service: "oregon-pulse-node" });
});

// Manual proxy using node-fetch
app.use("/api", async (req, res) => {
  const targetUrl = `${FASTAPI_URL}${req.originalUrl}`;
  console.log(`Proxying: ${req.originalUrl} -> ${targetUrl}`);

  try {
    const response = await fetch(targetUrl);
    const data = await response.json();
    res.status(response.status).json(data);
  } catch (err) {
    console.error("Proxy error:", err.message);
    res.status(502).json({ error: "FastAPI service unavailable" });
  }
});

app.listen(PORT, () => {
  console.log(`Node server running on http://localhost:${PORT}`);
  console.log(`Proxying /api requests to ${FASTAPI_URL}`);
});