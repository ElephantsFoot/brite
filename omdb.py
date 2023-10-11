import requests

from models import Movie

OMDP_API_URL = "http://www.omdbapi.com/"
APIKEY = "63786af"


class CannotGetMovie(Exception):
    pass


def get_movie_from_omdb(title: str, year: str | None = None) -> Movie:
    payload = {"apikey": APIKEY, "t": title}
    if year:
        payload["y"] = year
    r = requests.get(OMDP_API_URL, params=payload)
    movie_info = r.json()
    if movie_info["Response"] == "False":
        raise CannotGetMovie("Could not get movie")
    return Movie(
        title=movie_info["Title"],
        description=movie_info["Plot"],
        year=int(movie_info["Year"]),
    )
