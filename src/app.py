import os
from flask import Flask, jsonify, request
import json
import logging

from src.services.movie_service import MovieService


app = Flask(__name__)

movie_service = MovieService()

#Create a logs directory if it doesn't exist
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # Level of the logs to display (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Display logs in the console
        logging.FileHandler(os.path.join(log_dir, "watchit.log"))  #  Save logs to a file
    ]
)

# Create a logger object for the app
logger = logging.getLogger("WatchIT")

@app.route('/')
def index():
    """
    Root endpoint to welcome users to the API.

    Returns:
        JSON: A welcome message.
    """
    logger.info("Accessed root endpoint")
    return jsonify({"message": "Welcome to WatchIT!"})

@app.route('/movies')
def get_movies():
    """
    Endpoint to retrieve all movies.

    Returns:
        JSON: A list of movies.
    """
    logger.info("Fetching all movies")
    movies = movie_service.get_all_movies()
    return jsonify(movies)
    
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Endpoint to retrieve a specific movie by its ID.

    Args:
        movie_id (int): The ID of the movie to retrieve.

    Returns:
        JSON: The movie data if found, or an error message if not.
    """
    logger.info(f"Fetching movie with ID: {movie_id}")
    movie = movie_service.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie)
    
    logger.warning(f"Movie with ID {movie_id} not found")
    return jsonify({"error": "Movie not found"}), 404

@app.route('/movies', methods=['POST'])
def add_movie():
    """
    Endpoint to add a new movie to the list.

    Returns:
        JSON: The newly added movie data.
    """
    
    try:
        new_movie = request.get_json()
        logger.info(f"Attempting to add new movie: {new_movie}")
        added_movie = movie_service.add_movie(new_movie)
        logger.info(f"Successfully added movie with ID: {added_movie['id']}")
        return jsonify(added_movie), 201
    
    except ValueError as e:
        logger.error(f"Error adding movie: {e}")
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)