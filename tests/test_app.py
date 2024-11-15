import pytest
from src.app import app

@pytest.fixture
def client():
    """
    Fixture to provide a test client for the Flask app.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    with app.test_client() as client:
        yield client

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
    assert response.json['title'] == "The Godfather"

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