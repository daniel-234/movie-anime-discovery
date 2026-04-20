from datetime import date

from django.core.management.base import BaseCommand

from media.anilist import (
    AniListVariables,
    get_anime_list_from_api,
    get_manga_list_from_api,
)
from media.models import Anime, Manga, Movie
from media.tmdb import (
    get_movie_list_from_api,
)

TRENDING_MOVIES_OF_WEEK = "/trending/movie/week"

FETCH_TRENDING_MEDIA_QUERY = """
query ($type: MediaType, $page: Int) {
  Page(page: $page, perPage: 10) {
    media(type: $type, sort: TRENDING_DESC) {
      id
      type
      title { english romaji native }
      genres
      cover_image: coverImage { large }
      average_score: averageScore
      country_of_origin: countryOfOrigin
      status
      episodes
    }
  }
}
"""

FETCH_TRENDING_MANGA_QUERY = """
query ($type: MediaType, $page: Int) {
  Page(page: $page, perPage: 10) {
    media(type: $type, sort: TRENDING_DESC) {
      id
      type
      title { english romaji native }
      genres
      cover_image: coverImage { large }
      average_score: averageScore
      country_of_origin: countryOfOrigin
      status
      episodes
    }
  }
}
"""


class Command(BaseCommand):
    help = "Cache the movies into the DB"

    def handle(self, *args, **options):
        trending_anime_vars = AniListVariables(type="ANIME", page=1)
        trending_manga_vars = AniListVariables(type="MANGA", page=1)
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
                title_data = anime.get("title") or {}
                title_english = title_data.get("english")
                title_romaji = title_data.get("romaji")
                title_native = title_data.get("native")

                canonical_title = title_english or title_romaji or title_native
                if not canonical_title:
                    self.stdout.write(f"Skipping id={anime['id']} — no title available")
                    continue
                Anime.objects.update_or_create(
                    media_id=anime["id"],
                    defaults={
                        "title": canonical_title,
                        "title_english": title_english,
                        "title_romaji": title_romaji,
                        "title_native": title_native,
                        "country_of_origin": anime["country_of_origin"],
                        "cover_image": anime["cover_image"]["large"],
                    },
                )

        if manga_list:
            print("\n\n\n\n")
            print(manga_list)
            for manga in manga_list:
                title_data = manga.get("title") or {}
                title_english = title_data.get("english")
                title_romaji = title_data.get("romaji")
                title_native = title_data.get("native")

                canonical_title = title_english or title_romaji or title_native
                if not canonical_title:
                    self.stdout.write(f"Skipping id={anime['id']} — no title available")
                    continue
                Manga.objects.update_or_create(
                    media_id=manga["id"],
                    defaults={
                        "title": canonical_title,
                        "title_english": title_english,
                        "title_romaji": title_romaji,
                        "title_native": title_native,
                        "country_of_origin": manga["country_of_origin"],
                        "cover_image": manga["cover_image"]["large"],
                    },
                )
