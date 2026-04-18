from typing import TypedDict

import httpx
from django.conf import settings

TMDB_TOKEN = settings.TMDB_TOKEN

TMDB_URL = "https://api.themoviedb.org/3"
ANILIST_API_URL = "https://graphql.anilist.co"

HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}"}


class Movie(TypedDict):
    adult: bool
    backdrop_path: str
    id: int
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
    id: int
    title: dict
    genres: list
    cover_image: dict
    score: int
    country_of_origin: str
    status: str
    episodes: int


def get_movie_list_from_api(endpoint: str) -> list[Movie] | None:
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


def get_anime_list_from_api(query: str, variables: str) -> list[Media] | None:
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
