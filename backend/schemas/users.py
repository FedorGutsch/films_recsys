from pydantic import BaseModel, Field, field_validator, EmailStr
from typing import Annotated, Optional
from datetime import datetime

# Размерность вектора зависит от выбранной E5-модели. 
# Для intfloat/multilingual-e5-large = 1024, для e5-base = 768, e5-small = 384
E5_VECTOR_DIM = 1024

class UserBase(BaseModel):
    id: int
    username: Annotated[str, Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_\-]+$", description="Имя пользователя")]
    email: Annotated[EmailStr, Field(description="Email адрес")]
    preference_vector: Annotated[list[float], Field(description="Вектор предпочтений (E5 эмбеддинг)")]
    is_active: bool = Field(default=True, description="Статус аккаунта")
    created_at: datetime = Field(default_factory=datetime.now)

    @field_validator('preference_vector', mode='before')
    @classmethod
    def validate_preference_vector(cls, value):
        if not isinstance(value, list):
            raise ValueError("Вектор предпочтений должен быть списком чисел")
        if len(value) != E5_VECTOR_DIM:
            raise ValueError(f"Длина вектора предпочтений должна быть ровно {E5_VECTOR_DIM} (стандарт E5)")
        try:
            return [float(v) for v in value]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Все элементы вектора должны быть числами: {e}")


class UserCreate(UserBase):
    id: Optional[int] = None
    password: Annotated[str, Field(min_length=8, max_length=128, description="Пароль для регистрации")]
    
    preference_vector: Optional[list[float]] = Field(default_factory=lambda: [0.0] * E5_VECTOR_DIM, exclude=True)
    created_at: datetime = Field(default_factory=datetime.now, exclude=True)


class UserRead(UserBase):
    preference_vector: Optional[list[float]] = Field(None, exclude=True)