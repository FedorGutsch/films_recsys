from pydantic import BaseModel, Field, field_validator, ValidationInfo
from typing import Annotated, Optional
from datetime import datetime

from scripts.strings_transformers import String_to_list_transformer
from backend.constants import Age_limits


class FilmBase(BaseModel):
    id: int
    title_ru: Annotated[
        str,
        Field(min_length=2, max_length=100, description="Название фильма на русском"),
    ]
    title_en: Annotated[
        str,
        Field(
            min_length=2, max_length=100, description="Название фильма на английском"
        ),
    ]
    year: Annotated[int, Field(ge=1930, description="Год выпуска")]
    rating_kp: Annotated[
        float, Field(ge=0.0, le=10.0, description="Рейтинг на кинопоиске")
    ]
    director: Annotated[list[str], Field(description="Режиссер(ы)")]
    actors: Annotated[list[str], Field(description="Список актеров")]
    country: Annotated[
        list[str], Field(description="Страны участвовавшие при создании")
    ]
    genre: Annotated[list[str], Field(description="Жанры")]
    plot: Annotated[str, Field(description="Сюжет")]
    duration: int
    poster_url: str
    age_limit: Age_limits

    @field_validator("year", mode="after")
    @classmethod
    def year_validator(cls, value):
        if value > datetime.now().year:
            raise ValueError("Год выпуска должен быть меньше или равен чем текущий")
        return value

    @field_validator("actors", "director", "country", "genre", mode="before")
    @classmethod
    def transform_to_list(cls, value, info: ValidationInfo):
        try:
            return String_to_list_transformer.transform(value)
        except Exception as e:
            field_name = info.field_name
            raise ValueError(
                f"Не удалось распарсить {field_name}: {e} \n Напишите значения в одну строку через запятую"
            ) from e


class FilmCreate(FilmBase):
    id: Optional[int] = None
    created_at: datetime = Field(default_factory=datetime.now)


class FilmRead(FilmBase):
    pass
