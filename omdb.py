import requests

OMDP_API_URL = "http://www.omdbapi.com/"
APIKEY = "63786af"


def get_movie_info(title: str, year: str | None = None):
    payload = {"apikey": APIKEY, "t": title}
    if year:
        payload["y"] = year
    r = requests.get(OMDP_API_URL, params=payload)
    return r.json()
