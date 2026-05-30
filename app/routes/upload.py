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


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    # Save file path
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Read CSV
    df = pd.read_csv(file_path)

    inserted = 0
    skipped = 0

    # Insert into database
    for _, row in df.iterrows():
        try:
            product = models.Product(
                name=row["name"],
                price=row["price"],
                stock=row["stock"]
            )
            db.add(product)
            inserted += 1

        except Exception:
            skipped += 1

    db.commit()

    return {
        "filename": file.filename,
        "rows_in_csv": len(df),
        "rows_inserted": inserted,
        "rows_skipped": skipped
    }