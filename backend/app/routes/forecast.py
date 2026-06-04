from fastapi import APIRouter
from sqlalchemy import text
from app.database import engine

import numpy as np
from sklearn.linear_model import LinearRegression
import random

router = APIRouter()

@router.get("/forecast/{product_name}")
def forecast(product_name: str):

    with engine.connect() as conn:

        result = conn.execute(
            text("""
                SELECT s.quantity
                FROM sales s
                JOIN products p ON s.product_id = p.id
                WHERE p.name = :name
                ORDER BY s.created_at
            """),
            {"name": product_name}
        )

        sales = [row.quantity for row in result]

    # If no sales data exists, generate demo history
    if len(sales) == 0:

        sales = [
            random.randint(50, 100),
            random.randint(60, 110),
            random.randint(70, 120),
            random.randint(80, 130),
            random.randint(90, 140),
        ]

    X = np.array(range(len(sales))).reshape(-1, 1)
    y = np.array(sales)

    model = LinearRegression()
    model.fit(X, y)

    next_day = np.array([[len(sales)]])
    prediction = model.predict(next_day)[0]

    return {
        "product": product_name,
        "sales_history": sales,
        "predicted_next": round(float(prediction), 2)
    }