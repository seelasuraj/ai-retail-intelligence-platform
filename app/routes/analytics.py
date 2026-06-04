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
@router.get("/total-stock")
def total_stock():

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT SUM(stock) FROM products")
        )

        total = result.scalar()

    return {
        "total_stock": total
    }
@router.get("/average-price")
def average_price():

    with engine.connect() as conn:
        result = conn.execute(
            text("SELECT AVG(price) FROM products")
        )

        avg_price = result.scalar()

    return {
        "average_price": round(avg_price, 2)
    }
@router.get("/top-products")
def top_products():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT name, price
                FROM products
                ORDER BY price DESC
                LIMIT 5
            """)
        )

        products = []

        for row in result:
            products.append({
                "name": row.name,
                "price": row.price
            })

    return products
@router.get("/low-stock")
def low_stock():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT name, stock
                FROM products
                WHERE stock < 20
                ORDER BY stock ASC
            """)
        )

        products = []

        for row in result:
            products.append({
                "name": row.name,
                "stock": row.stock
            })

    return products
@router.get("/summary")
def summary():

    with engine.connect() as conn:

        total_records = conn.execute(
            text("SELECT COUNT(*) FROM products")
        ).scalar()

        total_stock = conn.execute(
            text("SELECT SUM(stock) FROM products")
        ).scalar()

        average_price = conn.execute(
            text("SELECT AVG(price) FROM products")
        ).scalar()

        inventory_value = conn.execute(
            text("""
                SELECT SUM(price * stock)
                FROM products
            """)
        ).scalar()

    return {
        "total_records": total_records,
        "total_stock": total_stock,
        "average_price": round(average_price, 2),
        "inventory_value": inventory_value
    }
@router.get("/inventory-value")
def inventory_value():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT SUM(price * stock)
                FROM products
            """)
        )

        value = result.scalar()

    return {
        "inventory_value": value
    }
@router.get("/top-stock-products")
def top_stock_products():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT name, stock
                FROM products
                ORDER BY stock DESC
                LIMIT 5
            """)
        )

        products = []

        for row in result:
            products.append({
                "name": row.name,
                "stock": row.stock
            })

    return products
@router.get("/top-revenue")
def top_revenue():

    with engine.connect() as conn:
        result = conn.execute(
            text("""
                SELECT
                    name,
                    price * stock AS revenue
                FROM products
                ORDER BY revenue DESC
                LIMIT 5
            """)
        )

        products = []

        for row in result:
            products.append({
                "name": row.name,
                "revenue": row.revenue
            })

    return products
@router.get("/insights")
def insights():

    insights = []

    with engine.connect() as conn:

        highest_revenue = conn.execute(
            text("""
                SELECT name, price * stock AS revenue
                FROM products
                ORDER BY revenue DESC
                LIMIT 1
            """)
        ).fetchone()

        low_stock = conn.execute(
            text("""
                SELECT name
                FROM products
                WHERE stock < 20
                LIMIT 1
            """)
        ).fetchone()

    if highest_revenue:
        insights.append(
            f"{highest_revenue.name} generates the highest revenue."
        )

    if low_stock:
        insights.append(
            f"{low_stock.name} stock is running low."
        )

    return insights