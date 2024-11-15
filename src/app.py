import os
from flask import Flask, jsonify, request
import json

app = Flask(__name__)

# Load data from JSON file
def load_data():
    # Get the directory where this script is located
    base_dir = os.path.dirname(os.path.abspath(__file__))
    # Build the path to the JSON file
    file_path = os.path.join(base_dir, "data", "movies.json")
    with open(file_path, "r") as file:
        return json.load(file)


@app.route('/')
def index():
    return jsonify({"message": "Welcome to WatchIT!"})

@app.route('/movies')
def get_movies():
    movies = load_data()
    return jsonify(movies)
    
@app.route('/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movies = load_data()
    movie = next((m for m in movies if m['id'] == movie_id), None)
    if movie:
        return jsonify(movie)
    return jsonify({"error": "Movie not found"}), 404

@app.route('/movies', methods=['POST'])
def add_movie():
    new_movie = request.get_json()
    movies = load_data()
    new_movie['id'] = len(movies) + 1
    movies.append(new_movie)
    with open("src/data/movies.json", "w") as file:
        json.dump(movies, file, indent=4)
    return jsonify(new_movie), 201

if __name__ == '__main__':
    app.run(debug=True)