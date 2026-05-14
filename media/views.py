from collections import defaultdict

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from media.models import StreamingOffer
from media.services import get_offers_for_movie, get_saved_ids

from .models import Anime, Manga, Movie, SavedAnime, SavedManga, SavedMovie

POSTERS_PER_ROW = 5

CONTENT_TYPE_MAP: dict[str, tuple[type[Model], type[Model], str]] = {
    "movie": (Movie, SavedMovie, "movie"),
    "anime": (Anime, SavedAnime, "anime"),
    "manga": (Manga, SavedManga, "manga"),
}


OFFER_TYPE_LABELS = [
    (StreamingOffer.OfferType.FLATRATE, "Stream"),
    (StreamingOffer.OfferType.RENT, "Rent"),
    (StreamingOffer.OfferType.BUY, "Buy"),
    (StreamingOffer.OfferType.ADS, "Free with ads"),
    (StreamingOffer.OfferType.FREE, "Free"),
]


def _resolve(content_type: str) -> tuple[type[Model], type[Model], str]:
    """Translate a content-type slug into (content_model, saved_model, fk_name)."""
    if content_type not in CONTENT_TYPE_MAP:
        raise Http404(f"Unknown content type: {content_type}")
    return CONTENT_TYPE_MAP[content_type]


def home(request):
    # Evaluate the sliced queryset and pass a list of objects
    # to `get_saved_ids`. Otherwise Django turns it into a subquery
    # that match an unstable set.
    movie_list = list(Movie.objects.all()[:POSTERS_PER_ROW])
    anime_list = Anime.objects.all()[:POSTERS_PER_ROW]
    manga_list = Manga.objects.all()[:POSTERS_PER_ROW]

    _, saved_movie_model, movie_fk = _resolve("movie")

    context = {
        "movie_list": movie_list,
        "anime_list": anime_list,
        "manga_list": manga_list,
        "saved_movie_ids": get_saved_ids(
            request.user, saved_movie_model, movie_fk, movie_list
        ),
        "grid_cols_class": f"grid-cols-{POSTERS_PER_ROW}",
    }

    return render(request, "media/home.html", context)


def movie_detail(request, movie_slug):
    movie = get_object_or_404(Movie, slug=movie_slug)
    is_bookmarked = _is_bookmarked(request.user, "movie", movie)

    country_code = ""
    country_name = ""
    ordered_offers = []
    if request.user.is_authenticated:
        country = request.user.profile.country
        country_code = country.code
        country_name = country.name
        offers = get_offers_for_movie(movie, country_code)

        grouped = defaultdict(list)
        for offer in offers:
            grouped[offer.offer_type].append(offer)

        ordered_offers = [
            (label, grouped[offer_type])
            for offer_type, label in OFFER_TYPE_LABELS
            if grouped.get(offer_type)
        ]

    return render(
        request,
        "media/movie/detail.html",
        {
            "movie": movie,
            "is_bookmarked": is_bookmarked,
            "content_type": "movie",
            "country_code": country_code,
            "country_name": country_name,
            "ordered_offers": ordered_offers,
        },
    )


def anime_detail(request, anime_slug):
    anime = get_object_or_404(Anime, slug=anime_slug)
    is_bookmarked = _is_bookmarked(request.user, "anime", anime)
    return render(
        request,
        "media/anime/detail.html",
        {"anime": anime, "is_bookmarked": is_bookmarked, "content_type": "anime"},
    )


def manga_detail(request, manga_slug):
    manga = get_object_or_404(Manga, slug=manga_slug)
    is_bookmarked = _is_bookmarked(request.user, "manga", manga)
    return render(
        request,
        "media/manga/detail.html",
        {
            "manga": manga,
            "is_bookmarked": is_bookmarked,
            "content_type": "manga",
        },
    )


def _is_bookmarked(user, content_type: str, item) -> bool:
    """Return True if the user has bookmarked this item."""
    if not user.is_authenticated:
        return False
    _, saved_model, fk_name = _resolve(content_type)
    return saved_model.objects.filter(user=user, **{fk_name: item}).exists()


# Note: django-stubs is built for mypy; ty has known friction with
# view decorators (require_POST) and **dict unpacks into manager methods.
# The ty: ignore comments below are intentional, not code smells.
# See issue #38
@require_POST  # ty: ignore[invalid-argument-type]
@login_required
def toggle_bookmark(request: HttpRequest, content_type: str, slug: str) -> HttpResponse:
    content_model, saved_model, fk_name = _resolve(content_type)
    item = get_object_or_404(content_model, slug=slug)

    # Check if the model already exists
    queryset = saved_model.objects.filter(user=request.user, **{fk_name: item})

    if queryset.exists():
        queryset.delete()
        created = False
    else:
        saved_model.objects.create(user=request.user, **{fk_name: item})
        created = True

    return render(
        request,
        "media/_bookmark_button.html",
        {
            "item": item,
            "content_type": content_type,
            "is_bookmarked": created,
        },
    )
