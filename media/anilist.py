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


def _fetch_media_list(query: str, variables: AniListVariables) -> list[Media] | None:
    """
    Retrieve information for both Media types (anime or manga) from the API
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
