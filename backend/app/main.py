from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes import analytics, recommendations, forecast, restock, report

app = FastAPI(
    title="AI Retail Intelligence Platform",
    version="1.0.0"
)

# ✅ FINAL CORS CONFIG (FIXED FOR VERCEL + LOCAL + RENDER)
origins = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://ai-retail-intelligence-platform.vercel.app"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routers
app.include_router(upload_router)
app.include_router(analytics.router, prefix="/analytics", tags=["Analytics"])
app.include_router(recommendations.router, tags=["Recommendations"])
app.include_router(forecast.router, prefix="/forecast", tags=["Forecast"])
app.include_router(restock.router, tags=["Restock"])
app.include_router(report.router)

@app.get("/")
def root():
    return {"message": "API Running Successfully 🚀"}