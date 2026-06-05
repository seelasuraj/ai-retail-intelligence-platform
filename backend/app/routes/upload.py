from fastapi import APIRouter, UploadFile, File, Depends, HTTPException
import pandas as pd
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models
from io import StringIO

router = APIRouter(prefix="/upload", tags=["Upload"])


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/")
async def upload_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):

    try:
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode("utf-8")))
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV read error: {str(e)}")

    required_cols = {"name", "price", "stock"}
    if not required_cols.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"Missing columns: {required_cols}")

    try:
        # 🔥 FORCE FULL RESET (IMPORTANT FIX)
        db.query(models.Product).delete(synchronize_session=False)
        db.commit()

        # optional but SAFE: expire session cache
        db.expire_all()

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB reset error: {str(e)}")

    inserted = 0
    skipped = 0

    for _, row in df.iterrows():
        try:
            product = models.Product(
                name=str(row["name"]),
                price=float(row["price"]),
                stock=int(row["stock"])
            )
            db.add(product)
            inserted += 1
        except Exception:
            skipped += 1

    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"DB commit error: {str(e)}")

    return {
        "filename": file.filename,
        "rows": len(df),
        "inserted": inserted,
        "skipped": skipped,
        "message": "Upload successful 🚀"
    }