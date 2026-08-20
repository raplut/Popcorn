from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str

class MovieCreate(BaseModel):
    title: str
    genres: str
    release_year: int
    director: str
    actors: str