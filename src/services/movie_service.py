import logging
from pymongo import MongoClient

class MovieService:
    """
    Class that manages the business logic for movies.
    """
    def __init__(self, collection=None):

        self.logger = logging.getLogger("MovieService")
        
        if collection is None:
            # Connect to the MongoDB database
            self.client = MongoClient("mongodb://mongodb:27017/")
            self.db = self.client["watchit"]
            self.collection = self.db["movies"]
        else:
            self.collection = collection

    def get_all_movies(self):
        """
        Get all movies from MongoDB.
        
        Returns:
            list: List of all movies.
        """
        self.logger.info("Fetching all movies from MongoDB")
        return list(self.collection.find({}, {"_id": 0}))


    def get_movie_by_id(self, movie_id):
        """
        Get a movie by its ID from MongoDB.
        
        Args:
            movie_id (int): ID of the movie to retrieve.
        
        Returns:
            dict or None: Movie data if found, None otherwise.
        """
        self.logger.info(f"Fetching movie with ID {movie_id} from MongoDB")
        return self.collection.find_one({"id": movie_id}, {"_id": 0})

    def add_movie(self, new_movie):
        """
        Add a new movie to MongoDB.
        
        Args:
            new_movie (dict): Movie data to add.
        
        Returns:
            dict: The newly added movie data.
        
        Raises:
            ValueError: If the movie data is invalid.
        """
        self.logger.info(f"Adding new movie to MongoDB: {new_movie}")
        
        # Check if the movie data is valid
        required_fields = ["title", "genre", "rating"]
        for field in required_fields:
            if field not in new_movie:
                raise ValueError(f"Missing required field: {field}")
        if not (0 <= new_movie["rating"] <= 10):
            raise ValueError("Rating must be between 0 and 10")
        
        # Assign a new ID to the movie
        new_movie["id"] = self.collection.count_documents({}) + 1
        
        # Add the movie to the database
        result = self.collection.insert_one(new_movie)
        new_movie["_id"] = str(result.inserted_id)  # Convert _id to string
        return new_movie
