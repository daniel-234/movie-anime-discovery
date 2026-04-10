from datetime import date

from django.core.management.base import BaseCommand

from media.models import Movie
from media.tmdb import get_movie_list_from_api

TRENDING_MOVIES_OF_WEEK = "/trending/movie/week"


class Command(BaseCommand):
    help = "Cache the movies into the DB"

    def handle(self, *args, **options):
        movies = get_movie_list_from_api(TRENDING_MOVIES_OF_WEEK)
        if movies:
            for movie in movies:
                release_date = date.fromisoformat(movie["release_date"])
                Movie.objects.update_or_create(
                    movie_id=movie["id"],
                    defaults={"title": movie["title"], "release_date": release_date},
                )
