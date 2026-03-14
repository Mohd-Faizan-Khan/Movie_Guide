import pickle
from pathlib import Path
import pandas as pd

# Get project root directory
BASE_DIR = Path(__file__).resolve().parent.parent

# Locate models folder
models_path = BASE_DIR / "models"

# Load similarity matrix
with open(models_path / "similarity_matrix.pkl", "rb") as f:
    similarity_matrix = pickle.load(f)

# Load movie metadata
with open(models_path / "movies_metadata.pkl", "rb") as f:
    movies = pickle.load(f)


def recommend_movies(title: str, top_n: int = 5) -> pd.DataFrame:
    """
    Recommend similar movies based on cosine similarity.
    """

    title = title.lower()

    matches = movies[movies["title"].str.contains(title, case=False, na=False)]

    if matches.empty:
        return None

    idx = matches.index[0]

    similarity_scores = list(enumerate(similarity_matrix[idx]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    top_movies = similarity_scores[1:top_n+1]

    movie_indices = [i[0] for i in top_movies]
    scores = [i[1] for i in top_movies]

    results = movies.iloc[movie_indices][["title", "vote_average"]].copy()
    results["similarity_score"] = scores

    return results