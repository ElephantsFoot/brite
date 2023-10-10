import pytest
from fastapi.testclient import TestClient
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
    print(data)
    assert data["detail"] == "Movie already exist"
