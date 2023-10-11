import pytest
from fastapi.testclient import TestClient
from requests.auth import HTTPBasicAuth
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from database import get_db, Base
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}, poolclass=StaticPool, )
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# clean up the database between tests
@pytest.fixture()
def test_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


def test_create_movie(test_db):
    response = client.post("/movies/", json={"title": "Shrek"}, )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Shrek"
    assert data["year"] == 2001
    assert "id" in data
    movie_id = data["id"]

    response = client.get(f"/movies/{movie_id}")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Shrek"
    assert data["id"] == movie_id


def test_create_existing_movie(test_db):
    response = client.post("/movies/", json={"title": "Shrek"}, )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Shrek"
    assert data["year"] == 2001
    assert "id" in data

    response = client.post("/movies/", json={"title": "Shrek"}, )
    assert response.status_code == 400, response.text
    data = response.json()
    assert data["detail"] == "Movie already exist"


def test_delete_movie_no_auth(test_db):
    response = client.delete("/movies/42")
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Not authenticated"


def test_delete_movie_wrong_password(test_db):
    response = client.delete("/movies/42", auth=HTTPBasicAuth('stanleyjobson', 'wrong'))
    assert response.status_code == 401, response.text
    data = response.json()
    assert data["detail"] == "Incorrect email or password"


def test_delete_movie(test_db):
    response = client.post("/movies/", json={"title": "Shrek"}, )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Shrek"
    assert data["year"] == 2001
    assert "id" in data
    movie_id = data["id"]

    response = client.delete(f"/movies/{movie_id}", auth=HTTPBasicAuth('stanleyjobson', 'swordfish'))
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["ok"]


def test_delete_movie_not_found(test_db):
    response = client.delete("/movies/42", auth=HTTPBasicAuth('stanleyjobson', 'swordfish'))
    assert response.status_code == 404, response.text
    data = response.json()
    assert data["detail"] == "Movie not found"


def test_get_movies_list(test_db):
    response = client.post("/movies/", json={"title": "Shrek"}, )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Shrek"
    assert data["year"] == 2001
    assert "id" in data
    first_movie_id = data["id"]

    response = client.post("/movies/", json={"title": "Shrek 2"}, )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Shrek 2"
    assert data["year"] == 2004
    assert "id" in data
    second_movie_id = data["id"]

    response = client.get(f"/movies")
    assert response.status_code == 200, response.text
    data = response.json()
    assert data[0]["title"] == "Shrek"
    assert data[0]["id"] == first_movie_id
    assert data[1]["title"] == "Shrek 2"
    assert data[1]["id"] == second_movie_id
