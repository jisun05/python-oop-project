import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base 

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./app.db")

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()


def get_db():
    """
        DB session provider used with FastAPI Depends.
        Opens a session at request start and always closes it after the response.
    """
    db = SessionLocal()         
    try:
        yield db               
    finally:
        db.close()            