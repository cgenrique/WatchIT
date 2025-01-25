import pytest
from flask import json
from src.app import app, db
from src.services.user_service import UserService
from unittest.mock import patch
from src.app import blacklist


@pytest.fixture
def client():
    """
    Provide a test client for the Flask app.

    Yields:
        FlaskClient: A test client for the Flask application.
    """
    with app.test_client() as client:
        # Clean database before tests
        db["users"].delete_many({})
        yield client


def test_register(client):
    """
    Test user registration.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The success message is returned.
    """
    response = client.post("/register", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert b"Registration successful!" in response.data


def test_register_existing_user(client):
    """
    Test registering with an already existing username.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The error message is returned.
    """
    UserService(db["users"]).create_user("testuser", "password123")
    response = client.post("/register", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert b"Username already exists" in response.data


def test_login(client):
    """
    Test user login.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The token is returned.
    """
    UserService(db["users"]).create_user("testuser", "password123")
    response = client.post("/login", data={"username": "testuser", "password": "password123"})
    assert response.status_code == 200
    assert "access_token" in json.loads(response.data)


def test_login_invalid_credentials(client):
    """
    Test login with invalid credentials.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 401.
        The error message is returned.
    """
    response = client.post("/login", data={"username": "nonexistent", "password": "wrongpassword"})
    assert response.status_code == 401
    assert "Invalid credentials" in json.loads(response.data)["error"]


def test_add_movie_to_list(client):
    """
    Test adding a movie to a user's list.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The success message is returned.
    """
    UserService(db["users"]).create_user("testuser", "password123")
    token = client.post("/login", data={"username": "testuser", "password": "password123"}).json["access_token"]
    response = client.post(
        "/movies/add_to_list",
        headers={"Authorization": f"Bearer {token}"},
        json={"movie_id": 123, "list": "favorites"}
    )
    assert response.status_code == 200
    assert "Movie 123 added to favorites" in json.loads(response.data)["message"]


def test_remove_movie_from_list(client):
    """
    Test removing a movie from a user's list.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The success message is returned.
    """
    user_service = UserService(db["users"])
    user_service.create_user("testuser", "password123")
    user_service.add_movie_to_list("testuser", 123, "favorites")
    token = client.post("/login", data={"username": "testuser", "password": "password123"}).json["access_token"]

    response = client.post(
        "/movies/remove_from_list",
        headers={"Authorization": f"Bearer {token}"},
        json={"movie_id": 123, "list": "favorites"}
    )
    assert response.status_code == 200
    assert "Movie 123 removed from favorites" in json.loads(response.data)["message"]


def test_get_all_lists(client):
    """
    Test retrieving all user lists (favorites, watched, to_watch).

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 200.
        The response contains the expected lists.
    """
    # Create a user and add movies to each list
    user_service = UserService(db["users"])
    user_service.create_user("testuser", "password123")
    user_service.add_movie_to_list("testuser", 123, "favorites")
    user_service.add_movie_to_list("testuser", 456, "watched")
    user_service.add_movie_to_list("testuser", 789, "to_watch")

    # Get the access token
    token_response = client.post("/login", data={"username": "testuser", "password": "password123"})
    token = token_response.json["access_token"]

    # Mock the TMDB service to return movie details
    with patch("src.app.tmdb_service.get_movie_details") as mock_get_movie_details:
        def mock_response(movie_id):
            return {
                "id": movie_id,
                "title": f"Mocked Movie {movie_id}",
                "overview": f"This is a mocked movie with ID {movie_id}.",
                "poster_path": f"/mocked_poster_{movie_id}.jpg"
            }

        # Set the side effect of the mock to return the movie details
        mock_get_movie_details.side_effect = mock_response

        # Call the `/lists` endpoint with the `format=json` query parameter
        response = client.get(
            "/lists?format=json",
            headers={"Authorization": f"Bearer {token}"}
        )

        # Check the response
        assert response.status_code == 200
        lists = json.loads(response.data)
        assert "favorites" in lists
        assert "watched" in lists
        assert "to_watch" in lists
        assert 123 in [movie["id"] for movie in lists["favorites"]]
        assert 456 in [movie["id"] for movie in lists["watched"]]
        assert 789 in [movie["id"] for movie in lists["to_watch"]]

def test_get_all_lists_unauthorized(client):
    """
    Test accessing the `/lists` endpoint without authentication.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 401.
        The error message indicates unauthorized access.
    """
    response = client.get("/lists")
    assert response.status_code == 401
    assert b"Missing Authorization Header" in response.data


def test_register_and_login(client):
    """
    Test registering and logging in a user.

    Args:
        client: The test client fixture.

    Asserts:
        Both registration and login succeed.
        The token is returned after login.
    """
    # Register the user
    register_response = client.post("/register", data={"username": "newuser", "password": "password123"})
    assert register_response.status_code == 200
    assert b"Registration successful!" in register_response.data

    # Login the user
    login_response = client.post("/login", data={"username": "newuser", "password": "password123"})
    assert login_response.status_code == 200
    assert "access_token" in json.loads(login_response.data)


def test_revoked_token(client):
    """
    Test accessing an endpoint with a revoked token.

    Args:
        client: The test client fixture.

    Asserts:
        The status code is 401.
        The error message indicates the token is revoked.
    """
    user_service = UserService(db["users"])
    user_service.create_user("testuser", "password123")

    # Authenticate the user
    token_response = client.post("/login", data={"username": "testuser", "password": "password123"})
    token = token_response.json["access_token"]

    # Decode the token to extract the jti
    from flask_jwt_extended.utils import decode_token
    decoded_token = decode_token(token)
    jti = decoded_token["jti"]

    # Add the token to the blacklist
    blacklist.add(jti)

    # Try to access a protected endpoint with the revoked token
    response = client.get(
        "/lists",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 401
    assert "Token has been revoked" in json.loads(response.data)["error"]
