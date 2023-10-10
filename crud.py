from sqlalchemy.orm import Session

import models


def get_movies(db: Session, title: str | None = None, skip: int = 0, limit: int = 100):
    query = db.query(models.Movie)
    if title:
        query = query.filter(models.Movie.title.contains(title))
    return query.order_by(models.Movie.title).offset(skip).limit(limit).all()


def get_movie(db: Session, movie_id: int):
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def create_movie(db: Session, movie_info):
    db_movie = models.Movie(title=movie_info["Title"], year=int(movie_info["Year"]), description=movie_info["Plot"])
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return db_movie


def delete_movie(db: Session, movie_id: int):
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    db.delete(db_movie)
    db.commit()
