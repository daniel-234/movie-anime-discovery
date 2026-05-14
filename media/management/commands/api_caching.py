from datetime import date

from django.core.management.base import BaseCommand

from media.anilist import AniListVariables, _fetch_media_list
from media.models import Anime, Manga, Movie, MovieGenre
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
      format
      title { english romaji native }
      genres
      description
      cover_image: coverImage { large }
      average_score: averageScore
      country_of_origin: countryOfOrigin
      status
      episodes
      chapters
      volumes
      year: seasonYear
      start_date: startDate { year }
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
        anime_list = _fetch_media_list(FETCH_TRENDING_MEDIA_QUERY, trending_anime_vars)
        manga_list = _fetch_media_list(FETCH_TRENDING_MEDIA_QUERY, trending_manga_vars)

        if movies:
            for movie in movies:
                release_date = date.fromisoformat(movie["release_date"])
                movie_obj, _ = Movie.objects.update_or_create(
                    movie_id=movie["id"],
                    defaults={
                        "title": movie["title"],
                        "overview": movie.get("overview", ""),
                        "release_date": release_date,
                        "poster_path": movie["poster_path"],
                        "backdrop_path": movie["backdrop_path"],
                        "media_type": movie.get("media_type", ""),
                        "original_language": movie.get("original_language", ""),
                        "popularity": movie.get("popularity"),
                        "vote_average": movie.get("vote_average"),
                        "vote_count": movie.get("vote_count"),
                        "adult": movie.get("adult", False),
                    },
                )

                # genre_ids is M2M — the Movie row must exist first, so this
                # happens after update_or_create, not in `defaults`.
                genres = MovieGenre.objects.filter(genre_id__in=movie["genre_ids"])
                found_ids = {g.genre_id for g in genres}
                missing = set(movie["genre_ids"]) - found_ids
                if missing:
                    self.stdout.write(
                        f"Movie id={movie['id']}: unknown genre ids {missing}; "
                        f"run the genre sync"
                    )
                movie_obj.genre_ids.set(genres)

        if anime_list:
            self.create_media(Anime, anime_list)

        if manga_list:
            self.create_media(Manga, manga_list)

    def create_media(self, model, list_of_media):
        for media in list_of_media:
            title_data = media.get("title") or {}
            title_english = title_data.get("english")
            title_romaji = title_data.get("romaji")
            title_native = title_data.get("native")

            canonical_title = title_english or title_romaji or title_native
            if not canonical_title:
                self.stdout.write(f"Skipping id={media['id']} — no title available")
                continue

            # seasonYear is reliable for anime but often null for manga;
            # fall back to startDate.year.
            start_date = media.get("start_date") or {}
            year = media.get("year") or start_date.get("year")

            defaults = {
                "title": canonical_title,
                "title_english": title_english,
                "title_romaji": title_romaji,
                "title_native": title_native,
                "country_of_origin": media["country_of_origin"],
                "cover_image": media["cover_image"]["large"],
                "year": year,
                "format": media.get("format") or "",
                "description": media.get("description") or "",
            }

            # Anime and Manga diverge here: episodes vs chapters/volumes.
            if model is Anime:
                defaults["episodes"] = media.get("episodes")
            else:
                defaults["chapters"] = media.get("chapters")
                defaults["volumes"] = media.get("volumes")

            model.objects.update_or_create(
                media_id=media["id"],
                defaults=defaults,
            )
