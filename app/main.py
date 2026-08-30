#python -m uvicorn app.main:app --reload

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from . import models, schemas
from .recommender import genre_counter, get_liked_genres, score_movies, get_recommendations

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

@app.get("/movies")
def get_movies(db: Session = Depends(get_db)):
    return db.query(models.Movie).all()

@app.post("/users/{user_id}/likes/{movie_id}")
def like_movie(user_id: int, movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    #For errors
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    new_like = models.Like(
        user_id = user.id,
        movie_id = movie.id
    )

    db.add(new_like)
    db.commit()
    db.refresh(new_like)

    return new_like

@app.post("/users/{user_id}/watches/{movie_id}")
def watch_movie(user_id:int, movie_id: int, db: Session = Depends(get_db)):
    movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    user = db.query(models.User).filter(models.User.id == user_id).first()

    #For errors
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if movie is None:
        raise HTTPException(status_code=404, detail="Movie not found")
    
    new_watch = models.Watch(
        user_id = user.id,
        movie_id = movie.id
    )

    db.add(new_watch)
    db.commit()
    db.refresh(new_watch)

    return new_watch

@app.get("/users/{user_id}/likes")
def get_likes(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Like).filter(models.Like.user_id == user_id).all()

@app.get("/users/{user_id}/watches")
def get_watches(user_id: int, db: Session = Depends(get_db)):
    return db.query(models.Watch).filter(models.Watch.user_id == user_id).all()

@app.get("/users/{user_id}/recommendations")
def get_user_recommendations(user_id: int, db: Session = Depends(get_db)):

   user = db.query(models.User).filter(models.User.id == user_id).first()

   if user is None:
       raise HTTPException(status_code=404, detail="User not found")
   
   movies = db.query(models.Movie).all()

   genre_counts = get_liked_genres(user)

   recommendations = get_recommendations(movies, genre_counts, user)

   return recommendations