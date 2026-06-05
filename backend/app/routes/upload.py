from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from io import StringIO

router = APIRouter(prefix="/upload", tags=["Upload"])


# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        # Read file safely
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV Read Error: {str(e)}")

    # Validate columns (VERY IMPORTANT)
    required_cols = {"name", "price", "stock"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {required_cols}"
        )

    # Clear old data safely
    try:
        db.query(models.Product).delete()
        db.commit()
    except Exception as e:
        print("Delete error:", e)

    inserted = 0
    skipped = 0

    # Insert rows
    for _, row in df.iterrows():
        try:
            product = models.Product(
                name=str(row["name"]),
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
        "message": "Upload successful 🚀"
    }