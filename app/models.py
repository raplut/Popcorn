from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)

    likes = relationship("Like", back_populates="user")
    watches = relationship("Watch", back_populates="user")

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    genres = Column(String)
    release_year = Column(Integer)
    director = Column(String)
    actors = Column(String)

    likes = relationship("Like", back_populates="movie")
    watches = relationship("Watch", back_populates="movie")

class Like(Base):
    __tablename__ = "likes"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    user = relationship("User", back_populates="likes")
    movie = relationship("Movie", back_populates="likes")

class Watch(Base):
    __tablename__ = "watches"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    movie_id = Column(Integer, ForeignKey("movies.id"))

    movie = relationship("Movie", back_populates="watches")
    user = relationship("User", back_populates="watches")