from flask import Blueprint, request, jsonify
from model.recommender import AnimeRecommender
from service.jikan_fetcher import fetch_anime_info
import os

os.chdir('..')
recommender = AnimeRecommender(
    "model/vectorizer.pkl", "model/anime_vectors.pkl", "dataset/anime-dataset-2025.csv"
)

routes = Blueprint("routes", __name__)

@routes.route('/recommend', methods=["POST", "OPTIONS"])
def recommend():
    if request.method == "OPTIONS":
        # Handle preflight OPTIONS request
        response = jsonify({})
        response.status_code = 200
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3000')
        response.headers.add('Access-Control-Allow-Methods', 'POST, OPTIONS')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type')
        return response

    # Handle POST request
    try:
        data = request.json
        if not data or "mal_id" not in data:
            return jsonify({"error": "mal_id is required"}), 400

        mal_id = data.get("mal_id")
        anime_data = fetch_anime_info(mal_id)
        if not anime_data:
            return jsonify({"error": "Anime not found"}), 404

        results = recommender.recommend(anime_data["synopsis"], anime_data["genres"])
        return jsonify(results), 200

    except Exception as e:
        # Log the error for debugging
        print(f"Error in /recommend: {str(e)}")
        return jsonify({"error": "Internal server error"}), 500