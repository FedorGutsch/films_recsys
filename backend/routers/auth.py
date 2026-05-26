from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from backend.schemas.users import UserCreate, UserRead
#from backend.services.auth_service import register_user, login_user, get_current_user
from backend.database import get_db

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register", response_model=UserRead)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """
    Регистрация пользователя.
    Использует твою схему UserCreate с проверкой пароля.
    """
    #return register_user(db, data)

@router.post("/login")
def login(form_data: dict, db: Session = Depends(get_db)):
    """
    Вход. Возвращает токен (access_token).
    """
    #return login_user(db, form_data)

#@router.get("/me", response_model=UserRead)
#def me(current_user: dict = Depends(get_current_user)):
#    """Получить текущего пользователя"""
#    return current_user
