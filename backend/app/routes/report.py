from fastapi import APIRouter
from fastapi.responses import FileResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from app.database import SessionLocal
from app.models import Product
from datetime import datetime
import os

router = APIRouter(
    prefix="/report",
    tags=["Report"]
)

@router.get("/pdf")
def generate_pdf():

    filename = "retail_report.pdf"

    doc = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    today = datetime.now().strftime("%d-%b-%Y %H:%M")

    content.append(
        Paragraph(
            "AI Retail Intelligence Report",
            styles["Title"]
        )
    )

    content.append(
        Paragraph(
            f"Generated On: {today}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    db = SessionLocal()

    products = db.query(Product).all()

    total_products = len(products)

    total_stock = sum(
        p.stock for p in products
    )

    inventory_value = sum(
        p.stock * p.price
        for p in products
    )

    content.append(
        Paragraph(
            "EXECUTIVE SUMMARY",
            styles["Heading1"]
        )
    )

    content.append(
        Paragraph(
            f"Total Products: {total_products}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Total Stock: {total_stock}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Inventory Value: ₹{inventory_value:,.0f}",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 20))

    content.append(
        Paragraph(
            "Product Inventory",
            styles["Heading2"]
        )
    )

    for product in products:
        content.append(
            Paragraph(
                f"{product.name} | Price: ₹{product.price} | Stock: {product.stock}",
                styles["BodyText"]
            )
        )

    db.close()

    doc.build(content)

    return FileResponse(
        path=filename,
        filename=filename,
        media_type="application/pdf"
    )