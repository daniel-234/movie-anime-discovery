from datetime import timedelta

from django.db.models import QuerySet
from django.utils import timezone

from media.models import Movie, Service, StreamingOffer
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
    )
    if fresh_offers.exists():
        return fresh_offers

    data = get_watch_providers_for_movie(movie.movie_id)
    if data is None:
        return StreamingOffer.objects.filter(movie=movie, country=country)

    country_data = data.get(country, {})

    StreamingOffer.objects.filter(movie=movie, country=country).delete()

    for offer_type_key in StreamingOffer.OfferType.values:
        for provider in country_data.get(offer_type_key, []):
            try:
                service = Service.objects.get(tmdb_provider_id=provider["provider_id"])
            except Service.DoesNotExist:
                print(
                    f"Unknown service tmdb_provider_id={provider['provider_id']}; "
                    f"run sync_services"
                )
                continue

            StreamingOffer.objects.create(
                movie=movie,
                service=service,
                country=country,
                offer_type=offer_type_key,
            )

    return StreamingOffer.objects.filter(movie=movie, country=country)
