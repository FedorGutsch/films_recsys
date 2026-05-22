from pydantic import BaseModel, Field, field_validator
from typing import Annotated, Optional, Literal
from scripts.strings_transformers import String_to_list_transformer
from datetime import datetime


class FilmBase(BaseModel):
    title_ru: Annotated[str, Field(min_length=2, max_length=100, description="Название фильма на русском")]
    title_en: Annotated[str, Field(min_length=2, max_length=100, description="Название фильма на английском")]
    year: Annotated[int, Field(ge=1930, description='Год выпуска')]
    rating_kp: Annotated[float, Field(ge=0.0, le=10.0, description='Рейтинг на кинопоиске')]
    director: str
    actors: Annotated[list[str], Field(description='Список актеров')]
    
    
    @field_validator("year", mode='after')
    @classmethod
    def year_validator(cls, value):
        if value > datetime.now().year:
            raise ValueError('Год выпуска должен быть меньше или равен чем текущий')
        return value
    
    @field_validator('actors', mode='before')
    @classmethod
    def actor_to_list(cls, value):
        try:
            actors = String_to_list_transformer.transform()
            return actors
        except Exception as e:
            raise ValueError(f"Не удалось распарсить список актёров: {e} \n Напишите их в одну строку через запятую ") from e
    
    
class FilmCreate(FilmBase):
    pass

class FilmRead(FilmBase):
    pass
    