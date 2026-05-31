from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.get("/record-count")
def record_count():

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT COUNT(*) FROM products")
        )

        count = result.scalar()

    return {
        "total_records": count
    }