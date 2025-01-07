import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch movie posters
def fetch_poster(movie_id):
    try:
        url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        response = requests.get(url)
        data = response.json()
        return f"https://image.tmdb.org/t/p/w185/{data['poster_path']}"
    except Exception as e:
        return "https://via.placeholder.com/185?text=No+Image"

# Function to recommend movies
def recommend(movie):
    try:
        # Check if the movie exists in the dataset
        if movie not in movies['title'].values:
            st.error(f"The movie '{movie}' is not in the database.")
            return [], []
        
        # Find the index of the selected movie
        movie_index = movies[movies['title'] == movie].index[0]

        # Get similarity scores for the selected movie
        distances = similarity[movie_index]
        movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

        # Prepare recommendations
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

# Function to load pickle from a URL
def load_pickle_from_url(url):
    try:
        # Google Drive direct download URL
        file_id = url.split('=')[1]
        download_url = f'https://drive.google.com/file/d/19U23aQ947aR_8pljX09aZ8T-N_DkCJMx/view?usp=sharing}
        
        response = requests.get(download_url, stream=True)
        response.raise_for_status()  # Check for any errors in the response

        # Return the pickle content after downloading
        return pickle.loads(response.content)
    
    except Exception as e:
        st.error(f"Error downloading or loading pickle file from URL: {e}")
        return None


# Load similarity matrix from URL (first try)
similarity_url = "https://drive.google.com/uc?id=19U23aQ947aR_8pljX09aZ8T-N_DkCJMx&export=download"
similarity = load_pickle_from_url(similarity_url)

# If the URL fails, try loading locally
if similarity is None:
    try:
        with open("similarity.pkl", "rb") as file:
            similarity = pickle.load(file)
        print("File loaded successfully from local storage!")
    except Exception as e:
        st.error(f"Error loading the file locally: {e}")
        similarity = None

# Load movies data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Streamlit UI
st.title('Movie Recommender System')

# Dropdown for selecting a movie
selected_movie_name = st.selectbox(
    'What movie would you like to watch?',
    movies['title'].values
)

# Recommendation button
if st.button('Recommend'):
    if similarity is not None:
        names, posters = recommend(selected_movie_name)
        if names and posters:
            # Display recommended movies in columns
            cols = st.columns(5)
            for i, col in enumerate(cols):
                if i < len(names):
                    col.text(names[i])
                    col.image(posters[i])
    else:
        st.error("Similarity data could not be loaded. Please check the source file.")
