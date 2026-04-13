# React + Vite

This template provides a minimal setup to get React working in Vite with HMR and some ESLint rules.

Currently, two official plugins are available:

- [@vitejs/plugin-react](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react) uses [Oxc](https://oxc.rs)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react/blob/main/packages/plugin-react-swc) uses [SWC](https://swc.rs/)

## React Compiler

The React Compiler is not enabled on this template because of its impact on dev & build performances. To add it, see [this documentation](https://react.dev/learn/react-compiler/installation).

## Expanding the ESLint configuration

If you are developing a production application, we recommend using TypeScript with type-aware lint rules enabled. Check out the [TS template](https://github.com/vitejs/vite/tree/main/packages/create-vite/template-react-ts) for information on how to integrate TypeScript and [`typescript-eslint`](https://typescript-eslint.io) in your project.
# 🛡️ SimGuard - Real-time SIM Swap Fraud Prevention

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115.6-green.svg)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/React-18-blue.svg)](https://reactjs.org)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 📌 Overview

**SimGuard** is an API-powered fraud detection system that prevents SIM swap fraud in real-time for mobile money transactions. It integrates **3 CAMARA APIs** (SIM Swap, Device Swap, Number Verification) with an **Agentic AI engine** (Claude) to automatically block or approve transactions in under 2 seconds.

### The Problem
Over **$500 million** is lost annually across Africa due to SIM swap fraud. Current detection takes hours or days - by then, the money is gone. Mobile money agents unknowingly process fraudulent transactions with no real-time fraud intelligence.

### The Solution
SimGuard provides instant fraud detection before money leaves the victim's account, empowering agents with AI-driven decisions.

---

## 🚀 Features

| Feature | Description |
|---------|-------------|
| 🔍 **Real-time SIM Swap Detection** | Checks SIM swap status within 24h/7d via CAMARA API |
| 📱 **Device Swap Check** | Detects recent device changes (10-day history) |
| ✅ **Number Verification** | Validates phone number ownership via OAuth2 |
| 🤖 **Agentic AI Engine** | Claude-powered autonomous decisions with explanations |
| 👨‍💼 **Agent Portal** | React-based interface for mobile money workers |
| 📊 **Live Dashboard** | Real-time fraud statistics and alerts |
| ⚡ **Sub-2 Second Response** | Instant fraud decisions |

---

## 🏗️ Architecture
┌─────────────────────────────────────────────────────┐
│ React Frontend │
│ Dashboard | Transaction Monitor | Agent Portal │
└────────────────────┬────────────────────────────────┘
│ REST API
┌────────────────────▼────────────────────────────────┐
│ FastAPI Backend │
│ ┌──────────┐ ┌──────────┐ ┌──────────────────────┐ │
│ │Transaction│ │ Fraud │ │ Agentic AI Engine │ │
│ │ Service │ │ Detector │ │ (Claude-powered) │ │
│ └─────┬─────┘ └────┬─────┘ └──────────┬───────────┘ │
│ │ │ │ │
│ ┌─────▼─────────────▼──────────────────▼───────────┐ │
│ │ CAMARA API Gateway │ │
│ │ SIM Swap │ Number Verification │ Device Swap │ │
│ └──────────────────────────────────────────────────┘ │
│ │ │
│ ┌─────────────────────▼────────────────────────────┐ │
│ │ PostgreSQL (audit + transactions) │ │
│ └──────────────────────────────────────────────────┘ │
└───────────────────────────────────────────────────────┘

text

---

## 🛠️ Tech Stack

| Category | Technology |
|----------|------------|
| **Backend** | Python 3.11+, FastAPI, SQLAlchemy |
| **Frontend** | React 18, Vite, TailwindCSS |
| **AI Engine** | Anthropic Claude API |
| **CAMARA APIs** | Nokia Network as Code (SIM Swap, Device Swap, Number Verification) |
| **Database** | PostgreSQL / SQLite |
| **Deployment** | Docker, docker-compose |

---

## 📦 Installation

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker (optional)

### Clone & Setup

```bash
# Clone repository
git clone https://github.com/yourusername/simguard.git
cd simguard

# Backend setup
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

# Frontend setup
cd ../frontend
npm install
Environment Variables
Create .env file in backend directory:

env
# Nokia Network as Code
NAC_API_KEY=your-rapidapi-key-here

# Anthropic Claude API
ANTHROPIC_API_KEY=sk-ant-your-key-here

# Database
DATABASE_URL=sqlite:///./simguard.db

# App
APP_ENV=development
CORS_ORIGINS=http://localhost:5173
Run with Docker
bash
docker-compose up --build
Run Locally
bash
# Terminal 1 - Backend
cd backend
uvicorn app.main:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend
npm run dev
Open http://localhost:5173

🧪 Testing
API Endpoints
bash
# Health check
curl http://localhost:8000/

# Check transaction
curl -X POST http://localhost:8000/api/transactions \
  -H "Content-Type: application/json" \
  -d '{"phone_number":"+99999991000","amount":1000,"is_new_recipient":true}'

# Get dashboard stats
curl http://localhost:8000/api/dashboard/stats
Demo Test Cases
Scenario	Phone Number	Amount	New Recipient	Expected
Safe Transaction	+99999991001	$50	No	✅ APPROVED
Fraud Transaction	+99999991000	$1000	Yes	🔴 BLOCKED
Suspicious	+99999991000	$300	No	🟡 FLAGGED
📁 Project Structure
text
simguard/
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI entry point
│   │   ├── api/                 # REST endpoints
│   │   │   ├── transactions.py
│   │   │   ├── dashboard.py
│   │   │   └── fraud.py
│   │   ├── models/              # Database models
│   │   ├── services/            # Business logic
│   │   │   ├── camara.py        # CAMARA API client
│   │   │   ├── fraud_detector.py
│   │   │   └── ai_engine.py     # Claude AI integration
│   │   └── schemas/             # Pydantic schemas
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   │   ├── AgentPortal.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   └── FraudAlertFeed.jsx
│   │   └── main.jsx
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
🎯 Why This Wins
Requirement	Our Implementation
At least 1 CAMARA API	✅ 3 APIs (SIM Swap, Device Swap, Number Verification)
APIs across categories	✅ Identity + Device categories
Agentic AI/GenAI	✅ Claude-powered fraud decision engine
Real-world problem	✅ $500M+ SIM swap fraud in Africa
Working codebase	✅ Full-stack prototype
Agent-focused	✅ Mobile money agent portal
🔮 Future Roadmap
Integrate additional CAMARA APIs (Device Location, Roaming Status)

Expand to support M-Pesa, MoMo, Airtel Money, Orange Money

WebSocket real-time fraud alert dashboard

ML model for adaptive risk scoring

Pilot deployment with telecom partners in Kenya and Nigeria

🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

📄 License
MIT License - see LICENSE file for details.

📧 Contact
Project Link: https://github.com/yourusername/simguard

🙏 Acknowledgments
Nokia Network as Code for CAMARA APIs

Anthropic for Claude AI

Africa Ignite Hackathon

Built to stop SIM swap fraud. One transaction at a time. 🛡️

text

---

## How to Add to GitHub:

1. **Create `README.md`** in your project root folder
2. **Copy and paste** the entire markdown above
3. **Save** the file
4. **Commit and push** to GitHub:

```bash
git add README.md
git commit -m "Add README for SimGuard project"
git push origin main
Your GitHub repository will now have a professional, detailed README! 🚀

