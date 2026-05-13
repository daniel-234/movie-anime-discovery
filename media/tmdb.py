from typing import TypedDict

import httpx
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

TMDB_TOKEN = settings.TMDB_TOKEN

if not TMDB_TOKEN:
    raise ImproperlyConfigured("TMDB_TOKEN environment variable not set.")

TMDB_URL = "https://api.themoviedb.org/3"

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


class ServiceProvider(TypedDict):
    display_priority: int
    logo_path: str
    provider_name: str
    provider_id: int


class CountryOffers(TypedDict, total=False):
    link: str
    flatrate: list[ServiceProvider]
    rent: list[ServiceProvider]
    buy: list[ServiceProvider]
    ads: list[ServiceProvider]
    free: list[ServiceProvider]


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


def get_services_list_from_api(endpoint: str) -> list[ServiceProvider] | None:
    """
    Retrieve the list of streaming services from a TMDB API endpoint.
    """
    with httpx.Client(base_url=TMDB_URL, headers=HEADERS) as client:
        try:
            response = client.get(endpoint)
            response.raise_for_status()
            return response.json().get("results", [])
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Failed to fetch data for {endpoint}: {e}")
            return None


def get_watch_providers_for_movie(
    movie_id: int,
) -> dict[str, CountryOffers] | None:
    """
    Retrieve watch providers (streaming availability) for a single movie
    across all countries TMDB tracks.
    """
    endpoint = f"/movie/{movie_id}/watch/providers"
    with httpx.Client(base_url=TMDB_URL, headers=HEADERS) as client:
        try:
            response = client.get(endpoint)
            response.raise_for_status()
            return response.json().get("results", {})
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Failed to fetch watch providers for movie {movie_id}: {e}")
            return None
