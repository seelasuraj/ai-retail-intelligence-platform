from database import engine
from models import Base
import models  # IMPORTANT: ensures models are registered

Base.metadata.create_all(bind=engine)

print("Tables created successfully ")