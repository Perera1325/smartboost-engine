# 🚀 SmartBoost Engine

An ML-inspired content ranking, boost optimization, analytics, and SOC-style alert platform.

Built as a full backend system demonstrating:

- Machine Learning scoring
- Ranking + budget optimization
- Analytics dashboard
- API security
- Rate limiting
- Request logging
- Anomaly detection (SOC alerts)

Inspired by Meta-style feed ranking and WSO2 API security concepts.

---

## ✨ Features

### Core
- Post ranking using sigmoid ML scoring
- Boost budget allocation
- REST API (FastAPI)

### Analytics
- Metrics storage
- Ranking history
- Dashboard viewer

### Security
- API Key authentication
- Rate limiting
- Request logging

### SOC
- High boost anomaly detection
- Alert storage
- Alerts API

---

## 🏗 Architecture

See: docs/architecture.txt

---

## 📁 Project Structure

  smartboost-engine/
│
├── app/
│ ├── main.py
│ ├── routes.py
│ └── security.py
│
├── analytics/
│ ├── metrics.json
│ └── requests.log
│
├── alerts/
│ └── alerts.json
│
├── dashboard/
│ └── index.html
│
├── docs/
│ └── architecture.txt
│
└── README.md

 
---

## ▶ How to Run

### 1. Install

```bash
pip install fastapi uvicorn numpy
  


2. Start Server
cd app
uvicorn main:app --reload


Open:

http://127.0.0.1:8000/docs

🔐 API Key

Use this header for all endpoints:

x-api-key: smartboost123

📡 Endpoints

POST /rank
GET /metrics
GET /alerts

🧪 Example Request
{
  "posts": [[1,0],[0,1]],
  "users": [[1,1],[0,0]],
  "total_budget": 100
}

🎯 Educational Objective

This project demonstrates:

ML-style ranking systems

Optimization pipelines

Backend security

SOC alerting concepts

API Gateway thinking

Built as a learning project aligned with enterprise platforms such as WSO2.

👨‍💻 Author

Vinod Perera
Dual Degree Undergraduate (Computer Science + Electrical & Electronic Engineering)


Save.

---

## 🌐 STEP 3 — Dashboard polish (optional)

Open:

👉 `dashboard/index.html`

Change title line:

```html
<h2>SmartBoost SOC Dashboard</h2>
































