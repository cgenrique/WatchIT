import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the TMDb access token from the environment variables
TMDB_ACCESS_TOKEN = os.getenv("TMDB_ACCESS_TOKEN")
TMDB_BASE_URL = "https://api.themoviedb.org/3"

class TMDbService:
    """
    A service class for interacting with The Movie Database (TMDb) API.
    Provides methods for searching movies and retrieving detailed movie information.
    """
    def __init__(self):
        if not TMDB_ACCESS_TOKEN:
            raise ValueError("Access token for TMDb is missing")

    def search_movies(self, query):
        """
        Search for movies using the TMDb API.

        Args:
            query (str): Search term.

        Returns:
            list: List of movies from the TMDB API.
        """
        url = f"{TMDB_BASE_URL}/search/movie"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
        }
        params = {
            "query": query
        }
        response = requests.get(url, headers=headers, params=params)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        return response.json().get("results", [])

    def get_movie_details(self, movie_id):
        """
        Get detailed information about a movie by its ID.

        Args:
            movie_id (int): ID of the movie.

        Returns:
            dict: Movie details from the TMDb API.
        """
        url = f"{TMDB_BASE_URL}/movie/{movie_id}"
        headers = {
            "accept": "application/json",
            "Authorization": f"Bearer {TMDB_ACCESS_TOKEN}"
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code} - {response.text}")
        return response.json()
