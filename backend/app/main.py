from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.upload import router as upload_router
from app.routes import analytics
from app.routes import recommendations
from app.routes import forecast
from app.routes import restock
from app.routes import report

app = FastAPI(
    title="AI Retail Intelligence Platform",
    version="1.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register Routes
app.include_router(upload_router)

app.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)

app.include_router(
    recommendations.router,
    tags=["Recommendations"]
)

app.include_router(
    forecast.router,
    prefix="/forecast",
    tags=["Forecast"]
)

app.include_router(
    restock.router,
    tags=["Restock"]
)

@app.get("/")
def root():
    return {
        "message": "AI Retail Intelligence Platform API Running Successfully"
    }
app.include_router(
    report.router
)