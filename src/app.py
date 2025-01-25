from functools import wraps
from json import dumps
import os
from flask import Flask, g, json, jsonify, request
import logging
import tempfile
from pymongo import MongoClient
from flask_jwt_extended import JWTManager, get_jwt, jwt_required, get_jwt_identity, create_access_token
from flask import render_template, redirect, url_for, session
from services.tmdb_service import TMDbService
from services.user_service import UserService
from datetime import timedelta
import json 



# Flask application setup
app = Flask(__name__)

# Set for managing token blacklist
blacklist = set()

# JWT configuration
app.secret_key = os.getenv("JWT_SECRET_KEY")
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)  # Token expires in 1 hour
jwt = JWTManager(app)

# MongoDB setup
MONGO_URI = "mongodb://mongodb:27017" if os.getenv("DOCKERIZED") == "true" else "mongodb://localhost:27017"
client = MongoClient(MONGO_URI)
db = client["watchit_db"]

# Service initialization
tmdb_service = TMDbService() # Service to interact with TMDb API
user_service = UserService(db["users"]) # User management service



# Configure logging
if os.getenv("TEST_ENV"):
    # Temporary log file for test environments
    temp_log = tempfile.NamedTemporaryFile(delete=False, suffix=".log")
    log_file = temp_log.name
else:
    # Create a dedicated logs directory for production
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

# Before request: Inject user login status into global context
@app.before_request
def inject_user():
    g.user_logged_in = "token" in session


# Decorator for role-based access
def role_required(role):
    """
    Enforces that only users with a specific role can access the endpoint.
    """
    def decorator(func):
        @wraps(func)
        @jwt_required()
        def wrapper(*args, **kwargs):
            identity = get_jwt_identity()
            if identity.get("role") != role:
                return jsonify({"error": "Unauthorized"}), 403
            return func(*args, **kwargs)
        return wrapper
    return decorator

# Decorator for login required
def login_required(func):
    """
    Ensures the user is logged in by checking session for token.
    Redirects to login page if not logged in.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if "token" not in session:
            return redirect(url_for("login_view"))
        return func(*args, **kwargs)
    return wrapper


# Blacklist for storing revoked tokens
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    """
    Verifies if a token is revoked by checking the blacklist.
    """
    jti = jwt_payload["jti"]  # Unique identifier for a JWT
    return jti in blacklist

# Callback for revoked tokens
@jwt.revoked_token_loader
def revoked_token_callback(jwt_header, jwt_payload):
    """
    Returns an error message if a token is revoked.
    """
    return jsonify({"error": "Token has been revoked. Please log in again."}), 401


# User registration route
@app.route("/register", methods=["GET", "POST"])
def register_view():
    """
    Handles user registration.
    Allows users to register with a username and password.
    """
    if request.method == "POST":
        data = request.form
        username = data.get("username")
        password = data.get("password")

        if not username or not password:
            return render_template("register.html", error="Username and password are required"), 400

        result, status = user_service.create_user(username, password)
        if status == 201:
            return render_template("register.html", success="Registration successful! Please log in.")
        else:
            return render_template("register.html", error=result.get("error"))
        
    return render_template("register.html")


# Route to fetch user information
@app.route("/auth/me", methods=["GET"])
@jwt_required()
def me():
    """
    Fetches the details of the currently authenticated user.
    """
    try:
        identity = get_jwt_identity()
        logger.info(f"Raw token identity: {identity}")
        identity = json.loads(identity)  # Deserialize JSON into a dictionary
        logger.info(f"Deserialized identity: {identity}")

        user = user_service.get_user(identity["username"])
        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({"username": user["username"], "role": user["role"]}), 200
    except Exception as e:
        logger.error(f"Error in /auth/me: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


# Home route
@app.route('/')
def index():
    """
    Root endpoint to display the search page.
    """
    return render_template('index.html', title="Welcome to WatchIT")


# Login route
@app.route("/login", methods=["GET", "POST"])
def login_view():
    """
    Handles user login.
    Validates username and password, and returns a JWT upon success.
    """
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        try:
            data = request.form  
            username = data.get("username")
            password = data.get("password")

            if not username or not password:
                return jsonify({"error": "Username and password are required"}), 400

            # User authentication
            user = user_service.authenticate_user(username, password)
            if user:
                identity = dumps({"username": user["username"], "role": user["role"]}) 
                logger.info(f"Generated JWT identity: {identity}")
                token = create_access_token(identity=identity)
                return jsonify({"access_token": token}), 200

            # Invalid credentials
            return jsonify({"error": "Invalid credentials"}), 401
        except Exception as e:
            logger.error(f"Error during login: {e}")
            return jsonify({"error": "An unexpected error occurred"}), 500



# Logout Endpoint
@app.route("/logout", methods=["GET"])
@login_required
def logout_view():
    """
    Logs out the user by removing their session token.
    """
    session.pop("token", None)  # Remove token from session
    return jsonify({"message": "Logged out successfully"}), 200


# Movie search route
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
    
# Fetch movie details and user-specific list statuses
@app.route('/movies/details/<int:movie_id>', methods=['GET'])
@jwt_required(optional=True)
def movie_details(movie_id):
    """
    Retrieves detailed information about a specific movie
    and checks the user's list statuses for that movie.

    Args:
        movie_id (int): The ID of the movie to retrieve details for.

    Returns:
        Rendered HTML page with movie details and list statuses.
    """
    try:
        # Fetch movie details from TMDb API
        movie = tmdb_service.get_movie_details(movie_id)
        lists_status = {"favorites": False, "watched": False, "to_watch": False}

        # Check if the user is authenticated
        if get_jwt():
            identity = get_jwt_identity()
            username = json.loads(identity).get("username")
            user = user_service.get_user(username)
            if user:
                # Check if the movie is in the user's lists
                user_lists = user.get("lists", {})
                for list_name in lists_status.keys():
                    lists_status[list_name] = movie_id in user_lists.get(list_name, [])

        # Render the movie details page
        return render_template("details.html", movie=movie, lists_status=lists_status)
    except Exception as e:
        logger.error(f"Error in movie details: {e}")
        return jsonify({"error": "Unable to fetch movie details"}), 500

# Add a movie to a user's list
@app.route("/movies/add_to_list", methods=["POST"])
@jwt_required()
def add_to_list():
    """
    Adds a movie to a specified user list (e.g., favorites, watched, to_watch).

    Request Body (JSON):
        movie_id (int): The ID of the movie to add.
        list (str): The name of the list to add the movie to.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        data = request.json
        logger.info(f"Request data: {data}")

        # Validate request data
        movie_id = data.get("movie_id")
        list_name = data.get("list")
        if not movie_id or not list_name:
            return jsonify({"error": "Missing 'movie_id' or 'list' in request body"}), 400

        # Get user identity from JWT
        identity = get_jwt_identity()
        identity_dict = json.loads(identity) if isinstance(identity, str) else identity
        username = identity_dict.get("username")

        # Fetch the user
        user = user_service.get_user(username)
        if not user:
            return jsonify({"error": "User not found"}), 404

        # Add the movie to the specified list
        response = user_service.add_movie_to_list(username, int(movie_id), list_name)
        if "error" in response:
            return jsonify(response), 400

        return jsonify(response), 200
    except Exception as e:
        logger.error(f"Unexpected error in add_to_list: {e}")
        return jsonify({"error": str(e)}), 500

# Remove a movie from a user's list
@app.route("/movies/remove_from_list", methods=["POST"])
@jwt_required()
def remove_from_list():
    """
    Removes a movie from a specified user list (e.g., favorites, watched, to_watch).

    Request Body (JSON):
        movie_id (int): The ID of the movie to remove.
        list (str): The name of the list to remove the movie from.

    Returns:
        JSON response indicating success or failure.
    """
    try:
        data = request.json
        logger.info(f"Request data: {data}")

        # Validating request data
        movie_id = data.get("movie_id")  # Asegúrate de que sea un entero
        list_name = data.get("list")

        if not movie_id or not list_name:
            return jsonify({"error": "Missing 'movie_id' or 'list' in request body"}), 400

        # Get user identity from JWT
        identity = get_jwt_identity()
        if isinstance(identity, str):  # Deserializa si es una cadena
            identity_dict = json.loads(identity)
        else:
            identity_dict = identity  # Ya es un diccionario

        username = identity_dict.get("username")
        logger.info(f"Username: {username}")

        # Fetch the user
        user = user_service.get_user(username)
        if not user:
            logger.error("User not found")
            return jsonify({"error": "User not found"}), 404

        # Remove the movie from the specified list
        response = user_service.remove_movie_from_list(username, int(movie_id), list_name)
        if response.get("error"):
            logger.error(f"Error removing movie: {response['error']}")
            return jsonify(response), 400

        logger.info(f"Movie {movie_id} removed from {list_name} successfully")
        return jsonify({"message": f"Movie {movie_id} removed from {list_name}"}), 200

    except Exception as e:
        logger.error(f"Unexpected error in remove_from_list: {e}")
        return jsonify({"error": str(e)}), 500

# View movies in a specific user list
@app.route("/movies/list/<list_name>", methods=["GET"])
@login_required
def view_list(list_name):
    """
    Displays movies in a specific user list (e.g., favorites, watched, to_watch).

    Args:
        list_name (str): The name of the list to display.

    Returns:
        Rendered HTML page showing the list of movies.
    """
    token = session.get("token")
    if not token:
        return redirect(url_for("login_view"))

    # Get the user identity from the token
    identity_json = get_jwt_identity()
    identity = json.loads(identity_json)
    username = identity["username"]

    # Validate the list name
    if list_name not in ["favorites", "watched", "to_watch"]:
        return jsonify({"error": f"Invalid list name '{list_name}'"}), 400

    # Fetch the user and their list of movies
    user = user_service.get_user(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    movies = user.get("lists", {}).get(list_name, [])
    return render_template("list.html", movies=movies, list_name=list_name)


# Admin endpoint to create custom lists
@app.route("/admin/create_list", methods=["POST"])
@role_required("admin")
def create_custom_list():
    """
    Admin-only endpoint to create a custom list.

    Request Body (JSON):
        list_name (str): The name of the new custom list.

    Returns:
        JSON response indicating success or failure.
    """
    data = request.json
    list_name = data.get("list_name")
    if not list_name:
        return jsonify({"error": "List name is required"}), 400
    try:
        UserService.create_custom_list(list_name)
        return jsonify({"message": f"Custom list {list_name} created"}), 201
    except Exception as e:
        logger.error(f"Error creating custom list: {e}")
        return jsonify({"error": str(e)}), 500

# Display all user lists with detailed movie information
@app.route("/lists", methods=["GET"])
@jwt_required()
def lists_view():
    """
    Displays all user lists (favorites, watched, to_watch) with detailed movie information.

    Returns:
        Rendered HTML page with lists and movie details.
    """
    try:
        app.logger.info(f"Authorization Header: {request.headers.get('Authorization')}")

        # Get user identity from JWT
        identity = get_jwt_identity()
        app.logger.info(f"Identity from token: {identity}")

        if not identity:
            return jsonify({"error": "Unauthorized"}), 401

        identity_dict = identity if isinstance(identity, dict) else json.loads(identity)
        username = identity_dict.get("username")
        app.logger.info(f"Username: {username}")

        # Fetch the user from the database
        user = user_service.get_user(username)
        if not user:
            return jsonify({"error": "User not found"}), 404

        user_lists = user.get("lists", {})
        all_lists = {}

        # Fetch detailed movie information for each list
        for list_name, movie_ids in user_lists.items():
            all_lists[list_name] = []
            for movie_id in movie_ids:
                tmdb_response = tmdb_service.get_movie_details(movie_id)
                if tmdb_response:
                    all_lists[list_name].append(tmdb_response)
                    
        # Check for `format=json` query parameter
        if request.args.get("format") == "json":
            return jsonify(all_lists), 200

        # Render the lists page
        return render_template("lists.html", title="My Lists", lists=all_lists)
    except Exception as e:
        app.logger.error(f"Error in /lists: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
    
