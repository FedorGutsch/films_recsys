from pydantic import BaseModel, Field, ConfigDict

class DirectorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Имя и фамилия режиссера")

class DirectorCreate(DirectorBase):
    pass

class DirectorRead(DirectorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)