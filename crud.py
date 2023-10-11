from sqlalchemy.orm import Session

import models


def get_movies(db: Session, title: str | None = None, skip: int = 0, limit: int = 100) -> list[models.Movie]:
    query = db.query(models.Movie)
    if title:
        query = query.filter(models.Movie.title.contains(title))
    return query.order_by(models.Movie.title).offset(skip).limit(limit).all()


def get_movie(db: Session, movie_id: int) -> models.Movie | None:
    return db.query(models.Movie).filter(models.Movie.id == movie_id).first()


def create_movie(db: Session, movie: models.Movie) -> models.Movie:
    db.add(movie)
    db.commit()
    db.refresh(movie)
    return movie


def delete_movie(db: Session, movie_id: int) -> None:
    db_movie = db.query(models.Movie).filter(models.Movie.id == movie_id).first()
    db.delete(db_movie)
    db.commit()
