from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database import engine
from app import models

from app.routes.upload import router as upload_router
from app.routes import analytics, recommendations, forecast, restock, report

app = FastAPI(
    title="AI Retail Intelligence Platform",
    version="1.0.0"
)

# ✅ CORS FIX
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-retail-intelligence-platform.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ CREATE TABLES ON STARTUP (SAFE WAY)
@app.on_event("startup")
def startup():
    models.Base.metadata.create_all(bind=engine)

# Routes
app.include_router(upload_router)
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(recommendations.router, tags=["Recommendations"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(restock.router, tags=["Restock"])
app.include_router(report.router)

@app.get("/")
def root():
    return {"message": "API Running Successfully 🚀"}