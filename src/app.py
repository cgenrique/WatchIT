import os
from flask import Flask, jsonify, request
import logging
import tempfile
from pymongo import MongoClient
from services.movie_service import MovieService
from services.tmdb_service import TMDbService
from flask import render_template



app = Flask(__name__)

MONGO_URI = "mongodb://mongodb:27017" if os.getenv("DOCKERIZED") == "true" else "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["watchit_db"]

movie_service = MovieService(db["movies"])
tmdb_service = TMDbService()


#Create a logs directory if it doesn't exist
# Log directory configuration
if os.getenv("TEST_ENV"):
    # Archivo temporal exclusivo para logs en entorno de pruebas
    temp_log = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
    log_file = temp_log.name
else:
    # Directorio de logs estándar para producción
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, "watchit.log")

# Basic logging configuration
logging.basicConfig(
    level=logging.INFO,  # Level of the logs to display (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),  # Display logs in the console
        logging.FileHandler(log_file)  #  Save logs to a file
    ]
)

# Create a logger object for the app
logger = logging.getLogger("WatchIT")

@app.route('/')
def index():
    """
    Root endpoint to display the search page.
    """
    return render_template('index.html', title="Welcome to WatchIT")

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
        logger.info("Successfully added movie.")
        return jsonify(added_movie), 201
    
    except ValueError as e:
        logger.error(f"Error adding movie: {e}")
        return jsonify({"error": str(e)}), 400
    
@app.route('/movies/search', methods=['GET'])
def search_movies():
    """
    Endpoint to search for movies using the TMDb API.

    Query Parameters:
        query (str): Search term.

    Returns:
        JSON: List of movies matching the search term.
    """
    
    query = request.args.get("query")
    if not query:
        return render_template("index.html")
    

    try:
        movies = tmdb_service.search_movies(query)
        return render_template("index.html", movies=movies, query=query)
    except Exception as e:
        logger.error(f"Error searching for movies: {e}")
        return render_template("index.html", error=str(e))
    
@app.route('/movies/details/<int:movie_id>', methods=['GET'])
def movie_details(movie_id):
    """
    Endpoint to get detailed information about a specific movie.

    Args:
        movie_id (int): The TMDb ID of the movie.

    Returns:
        Rendered HTML: A page showing the movie details.
    """
    try:
        movie = tmdb_service.get_movie_details(movie_id)
        return render_template("details.html", movie=movie)
    except Exception as e:
        logger.error(f"Error fetching movie details: {e}")
        return render_template("error.html", error=str(e)), 500


@app.route('/movies/add_to_list', methods=['GET'])
def add_to_list():
    """
    Endpoint to add a movie to a specific list.

    Query Parameters:
        movie_id (int): The TMDb ID of the movie.
        list (str): The name of the list ("favorites", "watched", "to_watch").

    Returns:
        Rendered HTML: A confirmation message.
    """
    movie_id = request.args.get("movie_id")
    list_name = request.args.get("list")
    
    if not movie_id or not list_name:
        return render_template("error.html", error="Missing 'movie_id' or 'list' parameter"), 400

    try:
        movie = tmdb_service.get_movie_details(movie_id)
        movie_service.add_movie_to_list(movie, list_name)
        return render_template("success.html", message=f"Movie added to {list_name}!")
    except Exception as e:
        logger.error(f"Error adding movie to list: {e}")
        return render_template("error.html", error=str(e)), 500


@app.route('/movies/list/<list_name>', methods=['GET'])
def view_list(list_name):
    """
    Endpoint to view all movies in a specific list.

    Args:
        list_name (str): The name of the list ("favorites", "watched", "to_watch").

    Returns:
        Rendered HTML: A page showing all movies in the list.
    """
    try:
        movies = movie_service.get_movies_from_list(list_name)
        return render_template("list.html", movies=movies, list_name=list_name)
    except Exception as e:
        logger.error(f"Error fetching list {list_name}: {e}")
        return render_template("error.html", error=str(e)), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
