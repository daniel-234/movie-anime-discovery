from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone

from media.models import Movie, SavedMovie, Service, StreamingOffer
from media.tmdb import get_watch_providers_for_movie

CACHE_TTL = timedelta(days=7)


def get_offers_for_movie(movie: Movie, country: str) -> QuerySet[StreamingOffer]:
    """
    Return cached streaming offers for (movie, country).

    If the cache is fresh, returns immediately. If stale or missing, fetches from
    TMDB, replaces the rows for this (movie, country), and returns the new rows.
    """
    cutoff = timezone.now() - CACHE_TTL

    fresh_offers = StreamingOffer.objects.filter(
        movie=movie,
        country=country,
        fetched_at__gte=cutoff,
    ).select_related("service")

    if fresh_offers.exists():
        return fresh_offers

    data = get_watch_providers_for_movie(movie.movie_id)
    if data is None:
        return StreamingOffer.objects.filter(
            movie=movie, country=country
        ).select_related("service")

    country_data = data.get(country, {})

    # Gather every provider ID we might need
    provider_ids = {
        p["provider_id"]
        for ot in StreamingOffer.OfferType.values
        for p in country_data.get(ot, [])
    }

    # Run one query to fetch all the matching rows at once
    services_by_id = {
        s.tmdb_provider_id: s
        for s in Service.objects.filter(tmdb_provider_id__in=provider_ids)
    }

    offers_to_create = []
    for offer_type_key in StreamingOffer.OfferType.values:
        for provider in country_data.get(offer_type_key, []):
            service = services_by_id.get(provider["provider_id"])
            if service is None:
                print(
                    f"Unknown service tmdb_provider_id={provider['provider_id']}; "
                    f"run sync_services"
                )
                continue

            offers_to_create.append(
                StreamingOffer(
                    movie=movie,
                    service=service,
                    country=country,
                    offer_type=offer_type_key,
                )
            )
    StreamingOffer.objects.filter(movie=movie, country=country).delete()
    StreamingOffer.objects.bulk_create(offers_to_create)
    return StreamingOffer.objects.filter(movie=movie, country=country).select_related(
        "service"
    )


def get_saved_movies(user) -> QuerySet[SavedMovie]:
    """Return the user's bookmarked movies, newest first."""
    if not user.is_authenticated:
        return SavedMovie.objects.none()
    return SavedMovie.objects.filter(user=user).select_related("movie")
