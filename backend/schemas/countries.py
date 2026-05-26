from pydantic import BaseModel, Field, ConfigDict

class CountryBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Название жанра")

class CountryCreate(CountryBase):
    pass

class CountryRead(CountryBase):
    id: int
    model_config = ConfigDict(from_attributes=True)