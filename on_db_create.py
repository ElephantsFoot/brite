import logging

from database import SessionLocal
from models import Movie
from omdb import get_movie_from_omdb, CannotGetMovie


def get_init_movie_list() -> list[list[str]]:
    init_movies_list = []
    with open("init_db_movies.txt", "r") as f:
        for line in f.readlines():
            title_and_year = line.strip().strip(")").split(" (")
            init_movies_list.append(title_and_year)
    return init_movies_list


def populate_db() -> None:
    db = SessionLocal()
    try:
        s = db.query(Movie).count()
        if s == 0:
            init_movies_list = get_init_movie_list()
            for movie in init_movies_list:
                try:
                    new_movie = get_movie_from_omdb(movie[0], movie[1])
                except CannotGetMovie:
                    logging.warning("Could not get movie: %s", movie)
                    continue
                db.add(new_movie)
            db.commit()
    finally:
        db.close()

