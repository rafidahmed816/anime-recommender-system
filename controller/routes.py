from flask import Blueprint, request, jsonify
from model.recommender import AnimeRecommender
from service.jikan_fetcher import fetch_anime_info
from service.anilist_normalizer import normalize_anilist_data
recommender = AnimeRecommender(
    "model/vectorizer.pkl", "model/anime_vectors.pkl", "dataset/anime-dataset-2025.csv"
)

routes = Blueprint("routes", __name__)
@routes.route('/')  # This handles the root URL
def home():
    return "Welcome to Anime Recommender!"
@routes.route('/recommend', methods=["POST"])
def recommend():
    data = request.json
    anime_info = normalize_anilist_data(data)

    synopsis = anime_info["synopsis"]
    genres = anime_info["genres"]
    themes = anime_info["themes"]
    studios = anime_info["studios"]

    query = f"{synopsis} {genres} {themes} {studios}"
    results = recommender.recommend(synopsis, f"{genres} {themes} {studios}")
    
    return jsonify(results)