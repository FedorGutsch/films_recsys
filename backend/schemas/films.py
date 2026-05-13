from pydantic import BaseModel
from typing import Annotated, Optional, Literal

class FilmBase(BaseModel):
    pass

class FilmCreate(FilmBase):
    pass

class FilmRead(FilmBase):
    pass
    