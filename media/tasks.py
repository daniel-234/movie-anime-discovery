from datetime import date

from .models import Movie
from .tmdb import get_movie_list_from_api

TRENDING_MOVIES_OF_WEEK = "/trending/movie/week"


def sync_trending_movies() -> None:
    movies = get_movie_list_from_api(TRENDING_MOVIES_OF_WEEK)
    if movies:
        for movie in movies:
            release_date = date.fromisoformat(movie["release_date"])
            Movie.objects.update_or_create(
                movie_id=movie["id"],
                defaults={"title": movie["title"], "release_date": release_date},
            )


def get_movies():
    return Movie.objects.all()[:5]
