from fastapi import APIRouter
from app.database import SessionLocal
from app.models import Product

router = APIRouter(
    prefix="/restock",
    tags=["Restock"]
)

@router.get("/recommendations")
def get_recommendations():
    db = SessionLocal()

    products = db.query(Product).all()

    recommendations = []

    for p in products:

        if p.stock <= 20:
            status = "Restock Immediately"

        elif p.stock <= 50:
            status = "Low Stock"

        else:
            status = "Stock Sufficient"

        recommendations.append({
            "product": p.name,
            "stock": p.stock,
            "recommendation": status
        })

    db.close()

    return recommendations