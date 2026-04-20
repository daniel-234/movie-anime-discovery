from datetime import date

from django.core.management.base import BaseCommand

from media.models import Anime, Manga, Movie
from media.tmdb import (
    get_anime_list_from_api,
    get_manga_list_from_api,
    get_movie_list_from_api,
)

TRENDING_MOVIES_OF_WEEK = "/trending/movie/week"

FETCH_TRENDING_MEDIA_QUERY = """
query ($type: MediaType, $page: Int) {
  Page(page: $page, perPage: 5) {
    media(type: $type, sort: TRENDING_DESC) {
      id
      title { english }
      genres coverImage { large }
      averageScore countryOfOrigin 
      status episodes
    }
  }
}
"""


FETCH_TRENDING_MANGA_QUERY = """
query ($type: MediaType, $page: Int) {
  Page(page: $page, perPage: 10) {
    media(type: $type) {
      id
      title { english romaji native}
      genres coverImage { large }
      averageScore countryOfOrigin 
      status episodes
    }
  }
}
"""


class Command(BaseCommand):
    help = "Cache the movies into the DB"

    def handle(self, *args, **options):
        trending_anime_vars = f"{ {'type': 'ANIME', 'page': 1} }"
        trending_manga_vars = f"{ {'type': 'MANGA', 'page': 1} }"
        movies = get_movie_list_from_api(TRENDING_MOVIES_OF_WEEK)
        anime_list = get_anime_list_from_api(
            FETCH_TRENDING_MEDIA_QUERY, trending_anime_vars
        )
        manga_list = get_manga_list_from_api(
            FETCH_TRENDING_MANGA_QUERY, trending_manga_vars
        )

        if movies:
            for movie in movies:
                release_date = date.fromisoformat(movie["release_date"])
                Movie.objects.update_or_create(
                    movie_id=movie["id"],
                    defaults={
                        "title": movie["title"],
                        "release_date": release_date,
                        "poster_path": movie["poster_path"],
                        "backdrop_path": movie["backdrop_path"],
                    },
                )

        if anime_list:
            print(anime_list)
            for anime in anime_list:
                Anime.objects.update_or_create(
                    media_id=anime["id"],
                    defaults={
                        "title": anime["title"]["english"],
                        "country_of_origin": anime["country_of_origin"],
                        "cover_image": anime["cover_image"]["large"],
                    },
                )

        if manga_list:
            print("\n\n\n\n")
            print(manga_list)
            for manga in manga_list:
                title_data = manga.get("title") or {}
                title = (
                    title_data.get("english")
                    or title_data.get("romaji")
                    or title_data.get("native")
                )

                if not title:
                    # Skip entries with no usable title at all
                    self.stdout.write(
                        f"Skipping manga id={manga['id']} - no title available"
                    )
                    continue
                Manga.objects.update_or_create(
                    media_id=manga["id"],
                    defaults={
                        "title": title,
                        "country_of_origin": manga["country_of_origin"],
                        "cover_image": manga["cover_image"]["large"],
                    },
                )
