from fastapi import FastAPI, Depends, HTTPException, Request, status
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

import crud
import models
import schemas
from database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")

BASE_URL = "http://localhost:8000"


@app.post("/shorten", response_model=schemas.URLInfo, status_code=status.HTTP_201_CREATED)
def shorten_url(payload: schemas.URLCreate, db: Session = Depends(get_db)):
    original = str(payload.url).rstrip("/")

    # если уже сокращали — вернём существующий
    existing = crud.get_by_original(db, original)
    if existing:
        return schemas.URLInfo(
            code=existing.code,
            short_url=f"{BASE_URL}/{existing.code}",
            original_url=existing.original_url,
            created_at=existing.created_at,
            clicks=existing.clicks,
        )

    url = crud.create_url(db, original)
    return schemas.URLInfo(
        code=url.code,
        short_url=f"{BASE_URL}/{url.code}",
        original_url=url.original_url,
        created_at=url.created_at,
        clicks=url.clicks,
    )


@app.get("/{code}")
def redirect_to_original(code: str, db: Session = Depends(get_db)):
    url = crud.get_by_code(db, code)
    if not url:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")

    crud.increment_clicks(db, url)
    return RedirectResponse(url=url.original_url, status_code=status.HTTP_307_TEMPORARY_REDIRECT)


@app.get("/info/{code}", response_model=schemas.URLInfo)
def get_info(code: str, db: Session = Depends(get_db)):
    url = crud.get_by_code(db, code)
    if not url:
        raise HTTPException(status_code=404, detail="Короткая ссылка не найдена")
    return schemas.URLInfo(
        code=url.code,
        short_url=f"{BASE_URL}/{url.code}",
        original_url=url.original_url,
        created_at=url.created_at,
        clicks=url.clicks,
    )