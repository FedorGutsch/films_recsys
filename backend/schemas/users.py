from datetime import datetime
from math import isinf, isnan
from typing import Annotated, List, Optional

from pydantic import BaseModel, ConfigDict, Field, SecretStr, field_validator

EMBEDDING_DIM = 1024
SCORE_MIN, SCORE_MAX = 0.0, 10.0

# ---------------------------------------------------------------------------
# 1. БАЗОВЫЕ АЛИАСЫ 
# ---------------------------------------------------------------------------
LoginField = Annotated[
    str,
    Field(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_\-\.]+$", description="Логин пользователя")
]
PasswordField = Annotated[
    SecretStr,
    Field(min_length=8, max_length=128, description="Пароль")
]

# ---------------------------------------------------------------------------
# 2. КЛИЕНТСКИЕ МОДЕЛИ ВВОДА (Request DTOs)
# ---------------------------------------------------------------------------

class UserCreate(BaseModel):
    """Регистрация. Только учётка, без вектора."""
    login: LoginField
    password: PasswordField
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    @field_validator("password", mode="after")
    @classmethod
    def _check_password_strength(cls, v: SecretStr) -> SecretStr:
        pwd = v.get_secret_value()
        checks = [
            len(pwd) >= 8,
            any(c.isupper() for c in pwd),
            any(c.islower() for c in pwd),
            any(c.isdigit() for c in pwd),
        ]
        if not all(checks):
            raise ValueError("Пароль должен содержать: 8+ символов, заглавную, строчную букву и цифру")
        return v


class FilmScoreInput(BaseModel):
    """Единичная оценка фильма в опроснике или после просмотра."""
    film_id: int = Field(gt=0, description="ID фильма из каталога")
    score: float = Field(ge=SCORE_MIN, le=SCORE_MAX, description=f"Оценка от {SCORE_MIN} до {SCORE_MAX}")
    model_config = ConfigDict(extra="forbid")


class UserOnboardingRequest(BaseModel):
    """Шаг 2: Мини-опросник после регистрации. Запускает генерацию вектора."""
    ratings: List[FilmScoreInput] = Field(
        min_length=5, max_length=50,
        description="Минимум 5 оценок для стабильного холодного старта"
    )
    model_config = ConfigDict(extra="forbid")

    @field_validator("ratings", mode="after")
    @classmethod
    def _ensure_unique_films(cls, v: List[FilmScoreInput]) -> List[FilmScoreInput]:
        ids = [r.film_id for r in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Дубликаты film_id в одном запросе запрещены")
        return v


class UserRatingUpdateRequest(BaseModel):
    """Пакетное обновление оценок после получения рекомендаций."""
    ratings: List[FilmScoreInput] = Field(min_length=1, max_length=20)
    current_vector_version: int = Field(ge=0, description="Версия вектора для optimistic locking")
    model_config = ConfigDict(extra="forbid")

    @field_validator("ratings", mode="after")
    @classmethod
    def _no_duplicates_in_batch(cls, v: List[FilmScoreInput]) -> List[FilmScoreInput]:
        ids = [r.film_id for r in v]
        if len(ids) != len(set(ids)):
            raise ValueError("Повторные оценки одного фильма в пакете запрещены")
        return v

# ---------------------------------------------------------------------------
# 3. ВНУТРЕННИЕ / СЕРВИСНЫЕ МОДЕЛИ (Service DTOs)
# ---------------------------------------------------------------------------

class UserVectorInternal(BaseModel):
    """Внутренний контейнер вектора предпочтений. НИКОГДА не уходит в клиентский ответ."""
    vector: List[float] = Field(min_length=EMBEDDING_DIM, max_length=EMBEDDING_DIM)
    version: int = Field(default=0, ge=0)
    is_normalized: bool = Field(default=True, description="Флаг L2-нормализации (обязательно для cosine)")
    model_config = ConfigDict(extra="forbid")

    @field_validator("vector", mode="before")
    @classmethod
    def _validate_vector(cls, v: Optional[List[float]]) -> List[float]:
        if v is None:
            return [0.0] * EMBEDDING_DIM
        if len(v) != EMBEDDING_DIM:
            raise ValueError(f"Ожидаемая размерность: {EMBEDDING_DIM}, получено: {len(v)}")
        try:
            clean = [float(x) for x in v]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Нечисловые элементы в векторе: {e}")
        if any(isnan(x) or isinf(x) for x in clean):
            raise ValueError("Вектор содержит NaN или Inf значения")
        return clean

# ---------------------------------------------------------------------------
# 4. МОДЕЛИ ОТВЕТА (Response DTOs)
# ---------------------------------------------------------------------------

class UserRead(BaseModel):
    """Базовый публичный профиль. Вектор здесь отсутствует."""
    id: int
    login: str
    is_deleted: bool = False
    onboarding_completed: bool = False
    preferences_version: int = 0
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)


class UserOnboardingStatus(BaseModel):
    """Ответ после прохождения опросника. Содержит только метаданные состояния."""
    user_id: int
    onboarding_completed: bool = True
    preferences_version: int
    cold_start_ready: bool = True
    model_config = ConfigDict(from_attributes=True)