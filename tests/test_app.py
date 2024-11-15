import pytest
from src.app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to WatchIT!"}

def test_get_movies(client):
    response = client.get('/movies')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    
def test_get_movie(client):
    response = client.get('/movies/1')
    assert response.status_code == 200
    assert response.json['title'] == "The Godfather"

def test_get_movie_not_found(client):
    response = client.get('/movies/999')
    assert response.status_code == 404
    assert response.json['error'] == "Movie not found"

def test_add_movie(client):
    new_movie = {"title": "Tenet", "genre": "Sci-Fi", "rating": 7.8}
    response = client.post('/movies', json=new_movie)
    assert response.status_code == 201
    assert response.json['title'] == "Tenet"