from pydantic import BaseModel, Field, field_validator, SecretStr, ConfigDict
from typing import Annotated, Optional


EMBEDDING_DIM = 1024


# ---------------------------------------------------------------------------
# Вспомогательные функции
# ---------------------------------------------------------------------------

def validate_password_strength(password: SecretStr) -> SecretStr:
    """Проверка сложности пароля. Выбрасывает ValueError, если пароль слабый."""
    pwd = password.get_secret_value()
    errors = []
    if len(pwd) < 8:
        errors.append("минимум 8 символов")
    if not any(c.isupper() for c in pwd):
        errors.append("хотя бы одна заглавная буква")
    if not any(c.islower() for c in pwd):
        errors.append("хотя бы одна строчная буква")
    if not any(c.isdigit() or (not c.isalnum()) for c in pwd):
        errors.append("хотя бы одна цифра или спецсимвол")
    if errors:
        raise ValueError("Пароль не удовлетворяет требованиям: " + ", ".join(errors))
    return password


# ---------------------------------------------------------------------------
# (без флага is_deleted)
# ---------------------------------------------------------------------------

class UserBase(BaseModel):
    """Общие поля с валидацией логина."""
    login: Annotated[str, Field(
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_\-\.]+$",
        description="Логин (буквы, цифры, _, -, .)"
    )]

    @field_validator("login", mode="before")
    @classmethod
    def strip_login(cls, v: str) -> str:
        if isinstance(v, str):
            return v.strip()
        return v


class UserRead(UserBase):
    """Ответ API: публичные данные + флаг мягкого удаления."""
    id: int
    is_deleted: bool = Field(
        description="Признак мягкого удаления (true = пользователь удалён)"
    )
    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Клиентские модели ввода
# ---------------------------------------------------------------------------

class UserLogin(UserBase):
    """Данные для входа."""
    password: SecretStr = Field(
        min_length=8,
        max_length=128,
        description="Пароль"
    )


class UserCreate(UserBase):
    """Регистрация: только то, что присылает клиент."""
    password: SecretStr = Field(
        min_length=8,
        max_length=128,
        description="Пароль для регистрации"
    )

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: SecretStr) -> SecretStr:
        return validate_password_strength(v)


class UserUpdate(BaseModel):
    """Данные для обновления профиля (все поля опциональны).

    Поле `is_deleted` позволяет пользователю удалить свой аккаунт (soft delete).
    На уровне эндпоинта необходимо проверить, что пользователь меняет только свои данные.
    """
    login: Optional[str] = Field(
        default=None,
        min_length=3,
        max_length=50,
        pattern=r"^[a-zA-Z0-9_\-\.]+$",
        description="Новый логин"
    )
    password: Optional[SecretStr] = Field(
        default=None,
        min_length=8,
        max_length=128,
        description="Новый пароль"
    )
    is_deleted: Optional[bool] = Field(
        default=None,
        description="Установить True для удаления аккаунта (soft delete)"
    )

    @field_validator("login", mode="before")
    @classmethod
    def strip_login(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            return v.strip()
        return v

    @field_validator("password")
    @classmethod
    def validate_password_if_provided(cls, v: SecretStr | None) -> SecretStr | None:
        if v is not None:
            return validate_password_strength(v)
        return v


# ---------------------------------------------------------------------------
# Внутренняя модель для сервисного слоя
# ---------------------------------------------------------------------------

class UserCreateInternal(UserBase):
    """Модель, используемая сервисом после хеширования пароля и генерации вектора."""
    password_hash: str = Field(description="Хеш пароля (bcrypt/argon2)")
    preferences: list[float] = Field(
        default_factory=lambda: [0.0] * EMBEDDING_DIM,
        description="Вектор предпочтений размерности EMBEDDING_DIM"
    )
    is_deleted: bool = Field(
        default=False,
        description="Флаг мягкого удаления, по умолчанию False"
    )

    @field_validator("preferences", mode="before")
    @classmethod
    def validate_preferences(cls, v):
        if v is None:
            return [0.0] * EMBEDDING_DIM
        if not isinstance(v, (list, tuple)):
            raise ValueError("Вектор предпочтений должен быть списком")
        if len(v) != EMBEDDING_DIM:
            raise ValueError(f"Длина вектора должна быть ровно {EMBEDDING_DIM}")
        try:
            return [float(x) for x in v]
        except (TypeError, ValueError) as e:
            raise ValueError(f"Все элементы вектора должны быть числами: {e}")