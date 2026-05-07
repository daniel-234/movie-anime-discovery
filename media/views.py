from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_POST

from .models import Anime, Manga, Movie, SavedAnime, SavedManga, SavedMovie

POSTERS_PER_ROW = 5

CONTENT_TYPE_MAP: dict[str, tuple[type[Model], type[Model], str]] = {
    "movie": (Movie, SavedMovie, "movie"),
    "anime": (Anime, SavedAnime, "anime"),
    "manga": (Manga, SavedManga, "manga"),
}


def _resolve(content_type: str) -> tuple[type[Model], type[Model], str]:
    """Translate a content-type slug into (content_model, saved_model, fk_name)."""
    if content_type not in CONTENT_TYPE_MAP:
        raise Http404(f"Unknown content type: {content_type}")
    return CONTENT_TYPE_MAP[content_type]


def home(request):
    context = {
        "movie_list": Movie.objects.all()[:POSTERS_PER_ROW],
        "anime_list": Anime.objects.all()[:POSTERS_PER_ROW],
        "manga_list": Manga.objects.all()[:POSTERS_PER_ROW],
        "grid_cols_class": f"grid-cols-{POSTERS_PER_ROW}",
    }

    return render(request, "media/home.html", context)


def movie_detail(request, movie_slug):
    movie = get_object_or_404(Movie, slug=movie_slug)
    is_bookmarked = _is_bookmarked(request.user, "movie", movie)
    return render(
        request,
        "media/movie/detail.html",
        {
            "movie": movie,
            "is_bookmarked": is_bookmarked,
            "content_type": "movie",
        },
    )


def anime_detail(request, anime_slug):
    anime = get_object_or_404(Anime, slug=anime_slug)
    is_saved = (
        request.user.is_authenticated
        and SavedAnime.objects.filter(user=request.user, anime=anime).exists()
    )
    return render(
        request, "media/anime/detail.html", {"anime": anime, "is_saved": is_saved}
    )


def manga_detail(request, manga_slug):
    manga = get_object_or_404(Manga, slug=manga_slug)
    is_saved = (
        request.user.is_authenticated
        and SavedManga.objects.filter(user=request.user, manga=manga).exists()
    )
    return render(
        request, "media/manga/detail.html", {"manga": manga, "is_saved": is_saved}
    )


def _is_bookmarked(user, content_type: str, item) -> bool:
    """Return True if the user has bookmarked this item."""
    if not user.is_authenticated:
        return False
    _, saved_model, fk_name = _resolve(content_type)
    lookup = {"user": user, fk_name: item}
    return saved_model.objects.filter(**lookup).exists()  # type: ignore[invalid-argument-type]


@login_required  # type: ignore[no-matching-overload]
@require_POST  # type: ignore[invalid-argument-type]
def toggle_bookmark(request: HttpRequest, content_type: str, slug: str) -> HttpResponse:
    content_model, saved_model, fk_name = _resolve(content_type)
    item = get_object_or_404(content_model, slug=slug)

    lookup = {"user": request.user, fk_name: item}
    saved, created = saved_model.objects.get_or_create(**lookup)  # type: ignore[invalid-argument-type]
    if not created:
        saved.delete()

    return render(
        request,
        "media/_bookmark_button.html",
        {
            "item": item,
            "content_type": content_type,
            "is_bookmarked": created,
        },
    )
