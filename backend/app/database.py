"""
Base de datos v1: SQLite plano, sin Docker ni servidor de BD aparte.
Suficiente para un solo club y un módulo. Migrar a Postgres solo
cuando haya una razón real (más de un club, concurrencia, etc.).
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "sqlite:///./data/lsm.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def init_db():
    from app import models  # noqa: F401 asegura que los modelos se registren
    Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
