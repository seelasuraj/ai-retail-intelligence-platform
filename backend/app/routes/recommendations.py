from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

router = APIRouter()

@router.get("/recommendations")
def get_recommendations():

    results = []

    with engine.connect() as conn:
        data = conn.execute(text("SELECT name, stock FROM products"))

        for row in data:
            stock = row.stock

            # AI LOGIC (backend level)
            if stock < 5:
                status = "Critical"
                action = "Restock Immediately"
            elif stock < 10:
                status = "Low"
                action = "Restock Soon"
            else:
                status = "Good"
                action = "No Action Needed"

            suggested_order = max(50 - stock, 0)

            results.append({
                "name": row.name,
                "stock": stock,
                "status": status,
                "action": action,
                "suggested_order": suggested_order
            })

    return results