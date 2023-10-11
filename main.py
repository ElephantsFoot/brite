from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import crud
import database
import models
import schemas
from auth import get_current_username
from database import engine, get_db
from omdb import get_movie_from_omdb, CannotGetMovie
from on_db_create import populate_db

database.Base.metadata.create_all(bind=engine, checkfirst=True)
populate_db()

app = FastAPI()


@app.get("/movies/", response_model=list[schemas.Movie])
def read_movies(title: str | None = None, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)) -> list[models.Movie]:
    movies = crud.get_movies(db, title=title, skip=skip, limit=limit)
    return movies


@app.get("/movies/{movie_id}", response_model=schemas.Movie)
def read_movie_by_id(movie_id: int, db: Session = Depends(get_db)) -> models.Movie:
    movie = crud.get_movie(db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.post("/movies/", response_model=schemas.Movie)
def create_movie(movie: schemas.MovieCreate, db: Session = Depends(get_db)) -> models.Movie:
    movies = crud.get_movies(db, title=movie.title)
    if movies:
        raise HTTPException(status_code=400, detail="Movie already exist")
    try:
        movie = get_movie_from_omdb(movie.title, str(movie.year))
    except CannotGetMovie:
        raise HTTPException(status_code=400, detail="Cannot get info for this movie")
    return crud.create_movie(db, movie)


@app.delete("/movies/{movie_id}")
def delete_movie(
        username: Annotated[str, Depends(get_current_username)],
        movie_id: int,
        db: Session = Depends(get_db)
) -> dict[str, bool]:
    movie = crud.get_movie(db, movie_id=movie_id)
    if not movie:
        raise HTTPException(status_code=404, detail="Movie not found")
    crud.delete_movie(db, movie_id=movie_id)
    return {"ok": True}
