import logging
import os
import json

class MovieService:
    """
    Class that manages the business logic for movies.
    """
    def __init__(self):
        # Get the directory where this script is located
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.file_path = os.path.join(self.base_dir, "../data/movies.json")
        self.logger = logging.getLogger("MovieService")


    def load_data(self):
        """
        Get movie data from the JSON file.

        Returns:
            list: List of movies loaded from the JSON file.
        """
        self.logger.info("Loading movie data from JSON file")        
        with open(self.file_path, "r") as file:
            return json.load(file)

    def save_data(self, movies):
        """
        Save movie data to the JSON file.

        Args:
            movies (list): List of movies to save.
        """
        self.logger.info("Saving movie data to JSON file")        
        with open(self.file_path, "w") as file:
            json.dump(movies, file, indent=4)

    def get_all_movies(self):
        """
        Get all movies.

        Returns:
            list: List of all movies.
        """
        return self.load_data()

    def get_movie_by_id(self, movie_id):
        """
        Get a movie by its ID.

        Args:
            movie_id (int): ID of the movie to retrieve.

        Returns:
            dict or None: Movie data if found, None otherwise.
        """
        movies = self.load_data()
        return next((m for m in movies if m['id'] == movie_id), None)

    def add_movie(self, new_movie):
        """
        Add a new movie.

        Args:
            new_movie (dict): Movie data to add.

        Returns:
            dict: The newly added movie data.
        
        Raises:
            ValueError: If the movie data is invalid.
        """
        # Check if the movie data is valid
        self.logger.info(f"Validating movie data: {new_movie}")        
        required_fields = ["title", "genre", "rating"]
        for field in required_fields:
            if field not in new_movie:
                self.logger.error(f"Missing required field: {field}")
                raise ValueError(f"Missing required field: {field}")
        
        # Check if the rating is between 0 and 10
        rating = new_movie["rating"]
        if not (0 <= rating <= 10):
            self.logger.error(f"Invalid rating: {new_movie['rating']}")
            raise ValueError("Rating must be between 0 and 10")
        
        # If the data is valid, add the movie
        movies = self.load_data()
        new_movie['id'] = len(movies) + 1
        movies.append(new_movie)
        self.save_data(movies)
        self.logger.info(f"Movie added successfully with ID: {new_movie['id']}")
        return new_movie
