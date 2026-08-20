from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Movie Recommendation API",
    description="An API that recommends movies based on your watch history, likes and, dislikes",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "API is running"
    }

@app.post("/users")
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):

    new_user = models.User(name=user.name)
    
    db.add(new_user) #Adds user to db
    db.commit() #Commit change
    db.refresh(new_user) #Needed to refresh object and add id num

    return new_user

@app.post("/movies")
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):

    new_movie = models.Movie(
        title = movie.title,
        genres = movie.genres,
        release_year = movie.release_year,
        director = movie.director,
        actors = movie.actors
    )

    db.add(new_movie)
    db.commit()
    db.refresh(new_movie)

    return new_movie