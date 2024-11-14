from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return jsonify({"message": "Welcome to WatchIT!"})

@app.route('/movies')
def get_movies():
    # Example movies data 
    return jsonify([
        {"id": 1, "title": "The Matrix", "genre": "Sci-Fi"},
        {"id": 2, "title": "Inception", "genre": "Action"},
    ])

if __name__ == '__main__':
    app.run(debug=True)