import streamlit as st
import pickle
import requests
import pandas as pd

# Function to fetch movie posters
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url)
        data = response.json()
        return f"https://image.tmdb.org/t/p/w185/{data.get('poster_path', '')}" if data.get('poster_path') else "https://via.placeholder.com/185?text=No+Image"
    except Exception:
        return "https://via.placeholder.com/185?text=No+Image"

# Function to recommend movies
def recommend(movie):
    try:
        if movie not in movies['title'].values:
            st.error(f"The movie '{movie}' is not in the database.")
            return [], []
        
        movie_index = movies[movies['title'] == movie].index[0]
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        recommended_movies = []
        recommended_movies_poster = []
        for i in movies_list:
            movie_id = movies.iloc[i[0]].movie_id
            recommended_movies.append(movies.iloc[i[0]].title)
            recommended_movies_poster.append(fetch_poster(movie_id))
        return recommended_movies, recommended_movies_poster
    except Exception as e:
        st.error(f"An error occurred during recommendation: {e}")
        return [], []

# Load movies data
try:
    movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
except Exception as e:
    st.error(f"Error loading movie dictionary: {e}")
    movies = pd.DataFrame()

# Load similarity matrix from URL
def load_pickle_from_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return pickle.loads(response.content)
    except Exception as e:
        st.error(f"Error loading similarity.pkl: {e}")
        return None

similarity_url = "https://drive.google.com/file/d/19U23aQ947aR_8pljX09aZ8T-N_DkCJMx/view?usp=sharing"
similarity = load_pickle_from_url(similarity_url)

# Streamlit UI
st.title('Movie Recommender System')

if not movies.empty and similarity is not None:
    # Dropdown for movie selection
    selected_movie_name = st.selectbox('What movie would you like to watch?', movies['title'].values)

    # Recommendation button
    if st.button('Recommend'):
        names, posters = recommend(selected_movie_name)
        if names and posters:
            cols = st.columns(len(names))
            for i, col in enumerate(cols):
                with col:
                    st.text(names[i])
                    st.image(posters[i])
        else:
            st.error("No recommendations available.")
else:
    st.error("Required data could not be loaded. Please check your files or URL.")
