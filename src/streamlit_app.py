import streamlit as st
import pickle
import requests
import pandas as pd
import os
import sys


# allow importing from src folder
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

API_URL = "http://127.0.0.1:5000/recommend"


# ---------- Load Movie Metadata ----------

with open("models/movies_metadata.pkl", "rb") as f:
    movies = pickle.load(f)


# ---------- API Call ----------

def get_recommendations(movie):

    response = requests.get(
        API_URL,
        params={"movie": movie}
    )

    if response.status_code == 200:
        data = response.json()
        return data["recommendations"]

    return None


# ---------- Page Configuration ----------
st.set_page_config(
    page_title="Movie Guide",
    page_icon="🎬",
    layout="centered"
)


# ---------- Header ----------
st.title("🎬 Movie Guide")
st.caption("Content-Based Movie Recommendation System using TF-IDF & Cosine Similarity")

st.divider()

# ---------- Input Section ----------
movie_list = [""] + sorted(movies["title"].str.title().unique())

movie_name = st.selectbox(
    "Select a movie",
    movie_list,
    index=0
)


# ---------- Recommendation Button ----------
if st.button("Recommend"):

    if not movie_name:
        st.warning("Please select a movie.")

    else:

        recommendations = get_recommendations(movie_name.lower())

        if recommendations is None:
            st.error("Movie not found or API error")

        else:
            st.subheader("Recommended Movies")

            df = pd.DataFrame(recommendations)

            df.insert(0, "Rank", range(1, len(df) + 1))
            df.rename(columns={
                "title": "Movie",
                "rating": "Rating"
            }, inplace=True)

            df["Rating"] = df["Rating"].round(1)

            # reorder columns
            df = df[["Rank", "Movie", "Rating"]]

            st.dataframe(df, use_container_width=True, hide_index = True)