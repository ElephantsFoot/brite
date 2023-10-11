from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import models
import schemas
from auth import get_current_username
from database import engine, get_db
from omdb import get_movie_info
from on_db_create import populate_db

models.Base.metadata.create_all(bind=engine, checkfirst=True)
populate_db()

app = FastAPI()


@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(title: str | None = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, title=title, skip=skip, limit=limit)
    return movies


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie_by_id(movie_id: int, db: Session = Depends(get_db)):
    movie = crud.get_movie(db, movie_id=movie_id)
    return movie


@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)):
    movies = crud.get_movies(db, title=movie.title)
    if movies:
        raise HTTPException(status_code=400, detail="Movie already exist")
    movie_info = get_movie_info(movie.title, movie.year)
    return crud.create_movie(db, movie_info)


@app.delete("/movies/{movie_id}")
def delete_movie(
        username: Annotated[str, Depends(get_current_username)],
        movie_id: int,
        db: Session = Depends(get_db)
):
    movie = crud.get_movie(db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    crud.delete_movie(db, movie_id=movie_id)
    return {"ok": True}
