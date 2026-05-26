from pydantic import BaseModel, Field, ConfigDict

class GenreBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Название жанра")

class GenreCreate(GenreBase):
    pass

class GenreRead(GenreBase):
    id: int
    model_config = ConfigDict(from_attributes=True)