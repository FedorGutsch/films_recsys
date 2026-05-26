from pydantic import BaseModel, Field, field_validator, ValidationInfo, ConfigDict
from typing import Annotated, Optional
from datetime import datetime

from scripts.strings_transformers import String_to_list_transformer
from backend.constants import Age_limits
from schemas.actors import ActorRead
from schemas.genres import GenreRead
from schemas.directors import DirectorRead
from schemas.countries import CountryRead


class FilmBase(BaseModel):
    title_ru: Annotated[
        str,
        Field(min_length=2, max_length=100, description="Название фильма на русском"),
    ]
    title_en: Annotated[
        Optional[str],
        Field(
            min_length=2, max_length=100, description="Название фильма на английском"
        ),
    ]
    year: Annotated[int, Field(ge=1930, description="Год выпуска")]
    rating_kp: Annotated[
        float, Field(ge=0.0, le=10.0, description="Рейтинг на кинопоиске")
    ]
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

class FilmCreate(FilmBase):
    directors: Annotated[list[str], Field(description="Режиссеры")]
    actors: Annotated[list[str], Field(description="Список актеров")]
    countries: Annotated[list[str], Field(description="Страны")]
    genres: Annotated[list[str], Field(description="Жанры")]
    created_at: datetime = Field(default_factory=datetime.now)


class FilmRead(FilmBase):
    id: int
    directors: list[DirectorRead]
    actors: list[ActorRead]
    countries: list[CountryRead]
    genres: list[GenreRead]
    model_config = ConfigDict(from_attributes=True)
