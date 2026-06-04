from fastapi import APIRouter, UploadFile, File, Depends
import pandas as pd
import os

from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models

router = APIRouter(
    prefix="/upload",
    tags=["Upload"]
)

UPLOAD_FOLDER = "app/uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# Database Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def upload_csv(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):

    # Save uploaded file
    file_path = os.path.join(
        UPLOAD_FOLDER,
        file.filename
    )

    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read CSV
    df = pd.read_csv(file_path)

    # Remove old records first
    try:
        db.query(models.Sale).delete()
    except:
        pass

    try:
        db.query(models.Product).delete()
    except:
        pass

    db.commit()

    inserted = 0
    skipped = 0

    # Insert fresh CSV data
    for _, row in df.iterrows():
        try:
            product = models.Product(
                name=row["name"],
                price=float(row["price"]),
                stock=int(row["stock"])
            )

            db.add(product)
            inserted += 1

        except Exception as e:
            print("Row Error:", e)
            skipped += 1

    db.commit()

    return {
        "filename": file.filename,
        "rows_in_csv": len(df),
        "rows_inserted": inserted,
        "rows_skipped": skipped,
        "message": "CSV uploaded successfully"
    }