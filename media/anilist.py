from typing import Literal, TypedDict

import httpx

ANILIST_API_URL = "https://graphql.anilist.co"


class Title(TypedDict):
    english: str | None
    romaji: str | None
    native: str | None


# Enforce that correct values must be passed to the API as variables
class AniListVariables(TypedDict):
    type: Literal["ANIME", "MANGA"]
    page: int


class Media(TypedDict):
    id: int
    title: Title
    genres: list
    cover_image: dict
    score: int
    country_of_origin: str
    status: str
    episodes: int


def get_anime_list_from_api(
    query: str, variables: AniListVariables
) -> list[Media] | None:
    """
    Retrieve anime information from a AniList API endpoint
    """
    with httpx.Client(base_url=ANILIST_API_URL) as client:
        try:
            # Check that "variables" is the correct type, as the API does not reject it
            # and it just treats every declared variable as null, failing silently.
            if not isinstance(variables, dict):
                raise TypeError(
                    f"variables must be a dict, got {type(variables).__name__}"
                )
            response = client.post("", json={"query": query, "variables": variables})
            response.raise_for_status()
            response_data = (
                response.json().get("data", {}).get("Page", {}).get("media", [])
            )
            expected_type = variables.get("type")
            if expected_type and any(
                m.get("type") != expected_type for m in response_data
            ):
                raise ValueError(
                    f"AniList returned mixed types; expected {expected_type!r}. "
                    f"Variables probably weren't applied. Payload: {variables!r}"
                )
            return response_data
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Failed to fetch data for {query}: {e}")
            return None


def get_manga_list_from_api(
    query: str, variables: AniListVariables
) -> list[Media] | None:
    """
    Retrieve manga information from a AniList API endpoint
    """
    with httpx.Client(base_url=ANILIST_API_URL) as client:
        try:
            if not isinstance(variables, dict):
                raise TypeError(
                    f"variables must be a dict, got {type(variables).__name__}"
                )
            response = client.post("", json={"query": query, "variables": variables})
            response.raise_for_status()
            response_data = (
                response.json().get("data", {}).get("Page", {}).get("media", [])
            )
            expected_type = variables.get("type")
            if expected_type and any(
                m.get("type") != expected_type for m in response_data
            ):
                raise ValueError(
                    f"AniList returned mixed types; expected {expected_type!r}. "
                    f"Variables probably weren't applied. Payload: {variables!r}"
                )
            return response_data
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            print(f"Failed to fetch data for {query}: {e}")
            return None
