import requests
import streamlit as st
import pickle
import pandas as pd


def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=37690f5ba331875db125b0338f9c2a9e')
    data = response.json()

    if 'poster_path' in data and data['poster_path']:
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return None


def recommend_movie(movie_name):
    if movie_name not in movies['title'].values:
        return ["Movie not found! Please select a different movie."]

    movie_index = movies[movies['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])

    recommend_movies = []
    recommended_movies_poster = []
    for i in movies_list[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

    return recommend_movies, recommended_movies_poster


st.title('Movie Recommender System')
movies = pickle.load(open('movies.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

if isinstance(movies, pd.Series):
    movies = pd.DataFrame(movies)

selected_movie_name = st.selectbox('Select Movie', movies['title'])

if st.button('Recommend Movie'):
    names, posters = recommend_movie(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    for i, col in enumerate([col1, col2, col3, col4, col5]):
        with col:
            st.text(names[i])
            poster_url = posters[i]
            if poster_url:
                st.image(poster_url)
            else:
                st.image("URL_TO_DEFAULT_IMAGE")

