from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.films import FilmRead
#from backend.services.films_service import get_random_films, get_film_by_id
from backend.database import get_db

router = APIRouter(prefix="/films", tags=["Films"])

@router.get("/random", response_model=List[FilmRead])
def random_films(
    limit: int = Query(default=10, ge=1, le=20), 
    db: Session = Depends(get_db)
):
    """
    Получить случайные фильмы для прохождения опросника (Onboarding).
    Использует твою модель FilmRead.
    """
    #return get_random_films(db, limit)

@router.get("/{film_id}", response_model=FilmRead)
def get_film(film_id: int, db: Session = Depends(get_db)):
    """Детали конкретного фильма"""
    #return get_film_by_id(db, film_id)