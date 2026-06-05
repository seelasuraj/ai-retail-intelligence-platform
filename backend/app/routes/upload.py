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
        # Read file safely (handles encoding issues)
        contents = await file.read()

        try:
            decoded = contents.decode("utf-8")
        except:
            decoded = contents.decode("latin-1")

        df = pd.read_csv(StringIO(decoded))

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"CSV Read Error: {str(e)}")

    # Clean column names (VERY IMPORTANT)
    df.columns = df.columns.str.strip().str.lower()

    # Validate columns
    required_cols = {"name", "price", "stock"}
    if not required_cols.issubset(set(df.columns)):
        raise HTTPException(
            status_code=400,
            detail=f"CSV must contain columns: {required_cols}. Found: {list(df.columns)}"
        )

    # Remove NaN rows (prevents crashes)
    df = df.dropna(subset=["name", "price", "stock"])

    # Clear old data safely
    try:
        db.query(models.Product).delete()
        db.commit()
    except Exception as e:
        print("Delete error:", e)

    inserted = 0
    skipped = 0

    # Insert rows safely
    for _, row in df.iterrows():
        try:
            product = models.Product(
                name=str(row["name"]).strip(),
                price=float(row["price"]),
                stock=int(row["stock"])
            )

            db.add(product)
            inserted += 1

        except Exception as e:
            print("Row Error:", e)
            skipped += 1

    try:
        db.commit()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"DB Commit Error: {str(e)}")

    return {
        "filename": file.filename,
        "rows_in_csv": len(df),
        "rows_inserted": inserted,
        "rows_skipped": skipped,
        "message": "Upload successful 🚀"
    }