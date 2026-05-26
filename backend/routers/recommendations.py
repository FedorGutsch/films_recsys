from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List
from backend.schemas.films import FilmRead
#from backend.services.recommendations_service import get_recommendations
from backend.database import get_db
#from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/recommendations", tags=["Recommendations"])

@router.get("/", response_model=List[FilmRead])
def get_recs(
    limit: int = Query(default=10),
    #current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Получить рекомендации на основе вектора preferences.
    """
    #return get_recommendations(db, current_user, limit)