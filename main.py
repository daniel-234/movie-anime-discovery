import httpx
from decouple import config

TMDB_URL = "https://api.themoviedb.org/3"
ANILIST_URL = "https://graphql.anilist.co"

TMDB_TOKEN = config("TMDB_TOKEN")

HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}"}

TRENDING_QUERY = """
query ($type: MediaType, $page: Int) {
  Page(page: $page, perPage: 5) {
    media(type: $type, sort: TRENDING_DESC) {
      id idMal type
      title { romaji english native }
      genres description coverImage { large }
      popularity averageScore countryOfOrigin status
      episodes chapters
    }
  }
}
"""

VARIABLES = f"{ {'type': 'ANIME', 'page': 1} }"


def _fetch_tmdb_data(endpoint: str) -> dict | None:
    """
    Retrieve information from a TMDB API endpoint
    """
    client = httpx.Client(base_url=TMDB_URL, headers=HEADERS)
    try:
        response = client.get(endpoint)
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Failed to fetch data for {endpoint}: {e.response.status_code}")
        return None
    except httpx.RequestError as e:
        print(f"Network error: {e}")
        return None


def _fetch_anilist_data(query: str, variables: str) -> dict | None:
    """
    Retrieve information from a AniList API endpoint
    """
    client = httpx.Client(base_url=ANILIST_URL)
    try:
        response = client.post("", json={"query": query, "variables": variables})
        response.raise_for_status()
        return response.json()
    except httpx.HTTPStatusError as e:
        print(f"Failed to fetch data for {query}: {e.response.status_code}")
        return None
    except httpx.RequestError as e:
        print(f"Network error: {e}")
        return None


def main():
    data = _fetch_tmdb_data("/trending/movie/week")
    anime = _fetch_anilist_data(TRENDING_QUERY, VARIABLES)
    print(data)
    print(anime)


if __name__ == "__main__":
    main()
