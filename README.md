# 🛒 AI Retail Intelligence Platform

> An end-to-end Decision Support System that transforms raw retail inventory data into actionable business intelligence — combining machine learning forecasting, smart restock recommendations, and Gemini-powered AI insights through a modern, interactive dashboard.

## 📸 Project Screenshots


### Dashboard Overview
![Dashboard Overview](./screenshots/dashboard-overview.png)

### Product Analytics
![Product Analytics](./screenshots/product-analytics.png)

### Revenue Analytics
![Revenue Analytics](./screenshots/revenue-analytics.png)

### Price Distribution
![Price Distribution](./screenshots/price-distribution.png)

### AI Forecast
![AI Forecast](./screenshots/ai-forecast.png)

### Restock Recommendations
![Restock Recommendations](./screenshots/restock-recommendations.png)

### PDF Report Generation
![PDF Report Generation](./screenshots/pdf-report.png)
---

## 🌐 Live Demo

**[ai-retail-intelligence-platform.vercel.app](https://ai-retail-intelligence-platform.vercel.app)**

---

## 🎯 The Problem This Solves

Most retail businesses accumulate vast amounts of inventory and sales data but continue making decisions based on intuition — resulting in stock-outs, excess inventory, and missed revenue opportunities.

This platform bridges that gap. Upload your sales CSV → get instant analytics, demand forecasts, restock recommendations, and plain-English AI insights — all in one place.

> 📄 This project is the practical implementation of my undergraduate research paper:
> **"Strategic Business Intelligence for Retail"** — Vardhaman College of Engineering, 2025
> Research validated on 50,000+ real retail transactions, achieving MAPE of 10.5% and reducing stock-out rates from 11.2% → 6.3%.

---

## ✨ Features

| Feature | Description |
|---|---|
| 📤 **CSV Upload** | Drag-and-drop inventory dataset upload with instant preview |
| 📊 **Inventory Analytics** | Total products, stock levels, average price, inventory value |
| 🔍 **Product Search** | Instant search across uploaded product catalog |
| ⚠️ **Low Stock Alerts** | Auto-detects products that need immediate attention |
| 📈 **Revenue Analysis** | Visual breakdown of top revenue-generating products |
| 🔮 **Demand Forecasting** | ML-based forecasting for future demand trends |
| 📦 **Restock Recommendations** | Smart suggestions based on stock levels and demand signals |
| 🤖 **AI Insights** | Gemini-powered plain-English business recommendations |
| 📄 **PDF Report Export** | One-click downloadable inventory analytics report |
| 🌙 **Modern Dark UI** | Responsive layout with animated cards and interactive charts |

---

## 🛠️ Tech Stack

```
Frontend    →  React 18 · Vite · Tailwind CSS · Recharts · Framer Motion · Axios
Backend     →  FastAPI · Python 3.11 · Uvicorn · SQLAlchemy
Database    →  PostgreSQL 15
ML / AI     →  Scikit-learn · Pandas · Gemini API
Deployment  →  Vercel (frontend) · Render (backend)
Dev Tools   →  Git · GitHub · Postman · VS Code
```

---

## 📁 Project Structure

```
ai-retail-intelligence-platform/
│
├── frontend/
│   └── src/
│       ├── components/         # Reusable UI components
│       ├── charts/             # Recharts visualizations
│       ├── pages/              # Dashboard, Upload, Forecast, Insights
│       ├── services/           # Axios API call functions
│       ├── App.jsx
│       └── App.css
│
├── backend/
│   └── app/
│       ├── routes/             # upload, analytics, forecast, restock, report
│       ├── models.py           # SQLAlchemy database models
│       ├── database.py         # DB connection and session management
│       └── main.py             # FastAPI app entry point
│
├── dataset/                    # Sample retail CSV for testing
├── screenshots/                # UI screenshots
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites
- Python 3.11+
- Node.js 18+
- PostgreSQL 15+

### 1. Clone the repository
```bash
git clone https://github.com/seelasuraj/ai-retail-intelligence-platform.git
cd ai-retail-intelligence-platform
```

### 2. Backend setup
```bash
cd backend
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env              # Add your credentials
uvicorn app.main:app --reload
```

### 3. Frontend setup
```bash
cd frontend
npm install
cp .env.example .env.local        # Add VITE_API_URL
npm run dev
```

### 4. Open in browser
```
Frontend  →  http://localhost:5173
API Docs  →  http://localhost:8000/docs
```

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/upload/` | Upload retail CSV, validate & store |
| `GET` | `/analytics/summary` | Total products, stock, price, value |
| `GET` | `/analytics/top-products` | Best performing products |
| `GET` | `/analytics/low-stock` | Products needing restock |
| `GET` | `/analytics/top-revenue` | Highest revenue products |
| `GET` | `/analytics/insights` | Gemini AI business insights |
| `GET` | `/forecast` | ML demand forecast |
| `GET` | `/restock/recommendations` | Smart restock suggestions |
| `GET` | `/report/pdf` | Generate downloadable PDF report |
| `GET` | `/health` | API health check |

> Full interactive API documentation auto-generated at `/docs` (Swagger UI).

---

## 📊 Analytics Provided

- Total Records · Total Stock · Average Price · Inventory Value
- Top Revenue Products · Low Stock Detection
- Revenue Distribution Charts · Demand Forecast Trends
- AI-Generated Business Recommendations

---

## 🔑 Environment Variables

```env
# backend/.env
DATABASE_URL=postgresql://user:password@localhost:5432/retail_db
GEMINI_API_KEY=your_gemini_api_key
SECRET_KEY=your_secret_key

# frontend/.env.local
VITE_API_URL=http://localhost:8000
```

---

## 🔭 Roadmap

- [ ] ARIMA & Apriori integration (research paper models)
- [ ] User authentication & multi-store support
- [ ] AWS S3 file storage
- [ ] Category-level filters
- [ ] Export to Excel
- [ ] Real-time inventory monitoring
- [ ] AI chat assistant

---

## 👤 Author

**Seela Venkata Naga Suraj**
B.Tech Computer Science (Data Science) · Vardhaman College of Engineering, Hyderabad
[LinkedIn](https://linkedin.com/in/seelasuraj) · [GitHub](https://github.com/seelasuraj)

---

## 📜 License

MIT License — free to use, modify, and build on this project.
