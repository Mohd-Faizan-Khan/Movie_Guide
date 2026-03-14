from flask import Flask, request, jsonify
import sys
import os

# allow importing from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from src.recommender import recommend_movies

app = Flask(__name__)

@app.route("/")
def home():
    return {"message": "Movie Recommendation API is running"}

@app.route("/recommend", methods=["GET"])
def recommend():

    movie = request.args.get("movie")

    try:
        recommendations = recommend_movies(movie)

        if recommendations is None:
            return jsonify({"error": "Movie not found"}), 404

        recommendations_list = recommendations["title"].str.title().tolist()

        return jsonify({
        "movie": movie,
        "recommendations": recommendations_list
    })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/recommend", methods=["POST"])
def recommend_post():

    data = request.get_json()

    if not data or "movie" not in data:
        return jsonify({"error": "Movie name required"}), 400

    movie = data["movie"]

    if not movie:
        return jsonify({"error": "Movie name required"}), 400

    recommendations = recommend_movies(movie)

    recommendations_list = recommendations["title"].str.title().tolist()

    return jsonify({
        "movie": movie,
        "recommendations": recommendations_list
    })


if __name__ == "__main__":
    app.run(debug=True)