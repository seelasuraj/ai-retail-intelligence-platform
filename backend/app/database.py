import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

# Get DATABASE_URL from environment (Render)
DATABASE_URL = os.getenv("DATABASE_URL")

# Fallback for safety (prevents crash)
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./test.db"

# SQLite needs this extra argument, PostgreSQL does not
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)