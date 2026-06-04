from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import analytics
from app.routes.upload import router as upload_router

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


@app.get("/")
def root():
    return {
        "message": "AI Retail Intelligence Platform API Running Successfully"
    }
app.include_router(
    analytics.router,
    prefix="/analytics",
    tags=["Analytics"]
)