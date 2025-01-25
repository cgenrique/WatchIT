from venv import logger
import bcrypt

class UserService:
    """
    Service class for managing user operations such as authentication,
    user creation, and updating user movie lists.
    """
    def __init__(self, users_collection):
        """
        Initialize the UserService with a MongoDB collection.

        Args:
            users_collection (Collection): MongoDB collection for storing user data.
        """
        self.users_collection = users_collection

    def create_user(self, username, password, role="user"):
        """
        Create a new user in the database.

        Args:
            username (str): The username of the new user.
            password (str): The password for the new user.
            role (str): The role of the user (default is 'user').

        Returns:
            dict: A success message or error details.
            int: The HTTP status code for the operation.
        """
        
        # Check if the username already exists
        if self.users_collection.find_one({"username": username}):
            return {"error": "Username already exists"}, 400
        
        # Hash the password before storing it
        password_hash = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())
        
        # Insert the new user into the database
        self.users_collection.insert_one({
            "username": username,
            "password_hash": password_hash,
            "role": role,
            "lists": {
                "favorites": [],
                "watched": [],
                "to_watch": []
            }
        })
        return {"message": "User created successfully"}, 201

    def authenticate_user(self, username, password):
        """
        Authenticate a user based on username and password.

        Args:
            username (str): The username of the user.
            password (str): The password provided by the user.

        Returns:
            dict or None: The user object if authentication is successful, or None otherwise.
        """
        
        # Find the user in the database by username
        user = self.users_collection.find_one({"username": username})
        
        # Verify the password using bcrypt
        if user and bcrypt.checkpw(password.encode("utf-8"), user["password_hash"]):
            return user
        
        return None

    def get_user(self, username):
        """
        Retrieve user information from the database.

        Args:
            username (str): The username of the user.

        Returns:
            dict: The user object with sensitive data removed, or None if the user is not found.
        """
        # Find the user in the database by username
        user = self.users_collection.find_one({"username": username}, {"password_hash": 0})
        
        # Convert ObjectId to string for JSON serialization
        if user and "_id" in user:
            user["_id"] = str(user["_id"])  # Convertir ObjectId a string
        return user

    def add_movie_to_list(self, username, movie_id, list_name):
        """
        Add a movie to a specific list for a user.

        Args:
            username (str): The username of the user.
            movie_id (int): The ID of the movie to add.
            list_name (str): The name of the list (e.g., 'favorites', 'watched', 'to_watch').

        Returns:
            dict: A success message or error details.
        """
        try:
            # Valdate list name
            if list_name not in ["favorites", "watched", "to_watch"]:
                return {"error": f"Invalid list name '{list_name}'"}

            # Add the movie to the specified list
            result = self.users_collection.update_one(
                {"username": username},
                {"$addToSet": {f"lists.{list_name}": movie_id}}
            )
            
            # Check if the user was found
            if result.matched_count == 0:
                return {"error": "User not found"}

            return {"message": f"Movie {movie_id} added to {list_name}"}
        except Exception as e:
            logger.error(f"Error in add_movie_to_list: {e}")
            return {"error": str(e)}


    
    def remove_movie_from_list(self, username, movie_id, list_name):
        """
        Remove a movie from a specific list for a user.

        Args:
            username (str): The username of the user.
            movie_id (int): The ID of the movie to remove.
            list_name (str): The name of the list (e.g., 'favorites', 'watched', 'to_watch').

        Returns:
            dict: A success message or error details.
        """
        
        # Validate list name
        if list_name not in ["favorites", "watched", "to_watch"]:
            return {"error": f"Invalid list name '{list_name}'"}, 400

        # Remove the movie from the specified list
        result = self.users_collection.update_one(
            {"username": username},
            {"$pull": {f"lists.{list_name}": movie_id}}
        )
        
        # Check if the movie was removed
        if result.matched_count > 0:
            return {"message": "Movie removed successfully"}
        return {"error": "User not found or movie not in list"}
