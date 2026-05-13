from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional, Literal

from datetime import datetime


class FilmBase(BaseModel):
    title_ru: Annotated[str, Field(min_length=2, max_length=100, description="Название фильма на русском")]
    title_en: Annotated[str, Field(min_length=2, max_length=100, description="Название фильма на английском")]
    year: Annotated[int, Field(ge=1930, description='Год выпуска')]
    rating_kp: Annotated[float, Field(ge=0.0, le=10.0, description='Рейтинг на кинопоиске')]
    director: str
    actors: Annotated[list[str], Field(description='Список актеров')]
    
    @field_validator("year", mode='after')
    def year_validator(cls, value):
        if value > datetime.now().year:
            raise ValueError('Год выпуска должен быть меньше или равен чем текущий')
        return value
    
    @field_validator('actors', mode='before')
    def actor_to_list():
        pass
    
    
class FilmCreate(FilmBase):
    pass

class FilmRead(FilmBase):
    pass
    