from sqlalchemy.orm import Session
from models import URL
from utils import encode_base62


def get_by_code(db: Session, code: str) -> URL | None:
    return db.query(URL).filter(URL.code == code).first()


def get_by_original(db: Session, original_url: str) -> URL | None:
    return db.query(URL).filter(URL.original_url == original_url).first()


def create_url(db: Session, original_url: str) -> URL:
    # сначала вставляем запись, чтобы получить id
    url = URL(code="", original_url=original_url)
    db.add(url)
    db.flush()  # получаем id без коммита

    # генерируем код на основе id — гарантированно уникально
    url.code = encode_base62(url.id)

    db.commit()
    db.refresh(url)
    return url


def increment_clicks(db: Session, url: URL) -> None:
    url.clicks += 1
    db.commit()