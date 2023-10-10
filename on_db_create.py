import logging

from database import SessionLocal
from models import Movie
from omdb import get_movie_info


def get_init_movie_list():
    init_movies_list = []
    with open("init_db_movies.txt", "r") as f:
        for line in f.readlines():
            title, year = line.strip().strip(")").split(" (")
            init_movies_list.append((title, year))
    return init_movies_list


def populate_db():
    db = SessionLocal()
    try:
        s = db.query(Movie).count()
        if s == 0:
            init_movies_list = get_init_movie_list()
            for movie in init_movies_list:
                movie_info = get_movie_info(movie[0], movie[1])
                if movie_info["Response"] == "False":
                    logging.warning("Could not get movie: %s", movie)
                    continue
                new_movie = Movie(
                    title=movie_info["Title"],
                    description=movie_info["Plot"],
                    year=int(movie_info["Year"]),
                )
                db.add(new_movie)
            db.commit()
    finally:
        db.close()

