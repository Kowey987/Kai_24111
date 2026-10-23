from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

# Для PostgreSQL:
# SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://user:pass@localhost/urls"
SQLALCHEMY_DATABASE_URL = "sqlite:///./urls.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # только для SQLite
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()