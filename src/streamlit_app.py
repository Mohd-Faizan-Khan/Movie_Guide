import streamlit as st
from recommender import recommend_movies


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
movie_name = st.text_input("Enter a movie name")


# ---------- Recommendation Button ----------
if st.button("Recommend"):

    if movie_name.strip() == "":
        st.warning("Please enter a movie name.")

    else:

        results = recommend_movies(movie_name)

        if results is None:
            st.error("Movie not found in dataset")

        else:
            st.subheader("Recommended Movies")
            # st.divider()

            results = results.copy()

            # Format movie titles
            results["title"] = results["title"].str.title()

            # Round ratings to 1 decimal
            results["vote_average"] = results["vote_average"].round(1)

            # Round similarity score to 3 decimals
            results["similarity_score"] = results["similarity_score"].round(3)

            # Rename columns
            results = results.rename(columns={
                "title": "Movie",
                "vote_average": "Rating",
                "similarity_score": "Similarity Score"
            })

            # Add ranking column
            results.insert(0, "Rank", range(1, len(results) + 1))

            # Reset index so DB index disappears
            results.reset_index(drop=True, inplace=True)

            # Display table
            st.table(results)