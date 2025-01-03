from pymongo import MongoClient
import pytest
from src.app import app, movie_service

@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask app.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    with app.test_client() as client:
        # Add initial data to the database
        movie_service.collection.insert_many([
            {"id": 1, "title": "Inception", "genre": "Sci-Fi", "rating": 8.8},
            {"id": 2, "title": "The Godfather", "genre": "Crime", "rating": 9.2}
        ])
        yield client


@pytest.fixture(autouse=True)
def clean_db():
    """
    Fixture to clean the MongoDB collection before each test.

    This ensures that tests start with an empty database.
    """
    movie_service.collection.delete_many({})  # Clear all documents in the movies collection


def test_index(client):
    """
    Test the root endpoint.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The response JSON contains the welcome message.
    """
    response = client.get('/')
    assert response.status_code == 200
    assert response.json == {"message": "Welcome to WatchIT!"}


def test_get_movies(client):
    """
    Test the endpoint to retrieve all movies.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The response JSON is a list.
    """
    response = client.get('/movies')
    assert response.status_code == 200
    assert isinstance(response.json, list)
    assert len(response.json) > 0  # Check that there's at least one movie


def test_get_movie(client):
    """
    Test the endpoint to retrieve a specific movie by ID.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The title of the movie matches the expected value.
    """
    response = client.get('/movies/1')
    assert response.status_code == 200
    assert response.json['title'] == "Inception"


def test_get_movie_not_found(client):
    """
    Test the endpoint to retrieve a movie with a non-existent ID.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 404.
        The response JSON contains an error message.
    """
    response = client.get('/movies/999')
    assert response.status_code == 404
    assert response.json['error'] == "Movie not found"


def test_add_movie(client):
    """
    Test the endpoint to add a new movie.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 201.
        The title of the new movie matches the input value.
    """
    new_movie = {"title": "Tenet", "genre": "Sci-Fi", "rating": 7.8}
    response = client.post('/movies', json=new_movie)
    assert response.status_code == 201
    assert response.json['title'] == "Tenet"


def test_add_movie_invalid_data(client):
    """
    Test adding a movie with missing fields.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 400.
        The response JSON contains an error message.
    """
    incomplete_movie = {"title": "Incomplete Movie"}
    response = client.post('/movies', json=incomplete_movie)
    assert response.status_code == 400
    assert "error" in response.json


def test_add_movie_invalid_rating(client):
    """
    Test adding a movie with an invalid rating.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 400.
        The response JSON contains an error message.
    """
    invalid_movie = {"title": "Invalid Rating", "genre": "Drama", "rating": 15}
    response = client.post('/movies', json=invalid_movie)
    assert response.status_code == 400
    assert "Rating must be between 0 and 10" in response.json["error"]


def test_add_movie_duplicate(client):
    """
    Test adding a duplicate movie.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 201 (duplicates are allowed since they have unique IDs).
    """
    duplicate_movie = {"title": "The Godfather", "genre": "Crime", "rating": 9.2}
    response = client.post('/movies', json=duplicate_movie)
    assert response.status_code == 201
    assert response.json['title'] == "The Godfather"
