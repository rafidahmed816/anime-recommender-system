import pickle
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

class AnimeRecommender:
    def __init__(self, vector_path, matrix_path, df_path):
        with open(vector_path, 'rb') as f:
            self.vectorizer = pickle.load(f)
        with open(matrix_path, 'rb') as f:
            self.anime_matrix = pickle.load(f)
        self.df = pd.read_csv(df_path)

    def recommend(self, synopsis, genres, top_n=5):
        query = synopsis + " " + genres
        query_vec = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vec, self.anime_matrix).flatten()

        # Get indices of top matches, sorted by similarity (excluding the top one)
        sorted_indices = similarities.argsort()[::-1]

        # Skip the first index (assumed to be the input anime itself)
        recommended_indices = sorted_indices[1:top_n + 1]

        return self.df.iloc[recommended_indices][["Mal_id", "Title", "Genres", "Synopsis"]].to_dict(orient="records")



