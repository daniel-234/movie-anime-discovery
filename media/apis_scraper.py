from typing import TypedDict

import httpx
from django.conf import settings

TMDB_TOKEN = settings.TMDB_TOKEN

TMDB_URL = "https://api.themoviedb.org/3"
ANILIST_API_URL = "https://graphql.anilist.co"

HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}"}

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


class Movie(TypedDict):
    adult: bool
    backdrop_path: str
    movie_id: int
    title: str
    overview: str
    poster_path: str
    media_type: str
    original_language: str
    genre_ids: list
    popularity: int
    release_date: str
    video: bool
    vote_average: int
    vote_count: int


class Media(TypedDict):
    media_id: int
    title: dict
    genres: list
    averageScore: int
    countryOfOrigin: str
    status: str
    episodes: int


def _fetch_tmdb_data(endpoint: str) -> list[Movie] | None:
    """
    Retrieve movie information from a TMDB API endpoint
    """
    with httpx.Client(base_url=TMDB_URL, headers=HEADERS) as client:
        try:
            response = client.get(endpoint)
            response.raise_for_status()
            return response.json().get("results", [])
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Failed to fetch data for {endpoint}: {e}")
            return None


def _fetch_anilist_media(query: str, variables: str) -> list[Media] | None:
    """
    Retrieve anime and manga information from a AniList API endpoint
    """
    with httpx.Client(base_url=ANILIST_API_URL) as client:
        try:
            response = client.post("", json={"query": query, "variables": variables})
            response.raise_for_status()
            response_data = (
                response.json().get("data", {}).get("Page", {}).get("media", [])
            )
            return response_data
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Failed to fetch data for {query}: {e}")
            return None


def main():
    trending_anime_vars = f"{ {'type': 'ANIME', 'page': 1} }"
    data = _fetch_tmdb_data("/trending/movie/week")
    anime = _fetch_anilist_media(FETCH_TRENDING_MEDIA_QUERY, trending_anime_vars)
    print(data)
    print("\n\n\n")
    print(anime)


if __name__ == "__main__":
    main()
