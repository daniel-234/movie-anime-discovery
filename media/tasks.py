from .models import Movie
from .tmdb import get_movie_list_from_api

TRENDING_MOVIES_OF_WEEK = "/trending/movie/week"


def sync_trending_movies() -> None:
    movies = get_movie_list_from_api(TRENDING_MOVIES_OF_WEEK)
    if movies:
        for movie in movies:
            Movie.objects.update_or_create(movie_id=movie["id"], title=movie["title"])


def get_movies():
    return Movie.objects.all()[:5]
