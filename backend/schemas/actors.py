from pydantic import BaseModel, Field, ConfigDict

class ActorBase(BaseModel):
    name: str = Field(min_length=1, max_length=100, description="Имя и фамилия актера")

class ActorCreate(ActorBase):
    pass

class ActorRead(ActorBase):
    id: int
    model_config = ConfigDict(from_attributes=True)