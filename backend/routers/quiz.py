from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.users import UserOnboardingRequest, UserOnboardingStatus
#from backend.services.quiz_service import submit_onboarding_ratings
from backend.database import get_db
#from backend.services.auth_service import get_current_user

router = APIRouter(prefix="/quiz", tags=["Quiz"])

@router.post("/submit", response_model=UserOnboardingStatus)
def submit_quiz(
    data: UserOnboardingRequest, 
    #current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Отправка оценок (10 фильмов).
    Принимает UserOnboardingRequest (список оценок).
    Сервис должен рассчитать вектор и сохранить в User.preferences.
    """
    #return submit_onboarding_ratings(db, current_user, data)