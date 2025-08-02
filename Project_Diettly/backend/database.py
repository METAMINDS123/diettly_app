# backend/database.py
from sqlmodel import SQLModel, create_engine

DATABASE_URL = "sqlite:///diettly.db"
engine = create_engine(DATABASE_URL, echo=True)

def init_db():
    SQLModel.metadata.create_all(engine)
