import os
from flask import Flask, jsonify, request
import json

from src.services.movie_service import MovieService

app = Flask(__name__)

movie_service = MovieService()

@app.route('/')
def index():
    """
    Root endpoint to welcome users to the API.

    Returns:
        JSON: A welcome message.
    """
    return jsonify({"message": "Welcome to WatchIT!"})

@app.route('/movies')
def get_movies():
    """
    Endpoint to retrieve all movies.

    Returns:
        JSON: A list of movies.
    """
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
    movie = movie_service.get_movie_by_id(movie_id)
    if movie:
        return jsonify(movie)
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
        added_movie = movie_service.add_movie(new_movie)
        return jsonify(added_movie), 201
    
    except ValueError as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)