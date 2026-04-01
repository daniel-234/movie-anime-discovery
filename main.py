from decouple import config
import httpx

TMDB_URL = "https://api.themoviedb.org/3"

TMDB_TOKEN = config("TMDB_TOKEN")

HEADERS = {"Authorization": f"Bearer {TMDB_TOKEN}"}

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
        print(
            f"Failed to fetch data for {endpoint}: {e.response.status_code}"
        )
        return None
    except httpx.RequestError as e:
        print(f"Network error: {e}")
        return None


def main():
    data = _fetch_tmdb_data("/trending/movie/week")
    print(data)


if __name__ == "__main__":
    main()
