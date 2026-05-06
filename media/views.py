from typing import Any

from django.contrib.auth.decorators import login_required
from django.db.models import Model
from django.http import Http404, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.http import require_POST

from .models import Anime, Manga, Movie, SavedAnime, SavedManga, SavedMovie

POSTERS_PER_ROW = 5


CONTENT_TYPE_MAP = {
    "movie": (Movie, SavedMovie, "movie"),
    "anime": (Anime, SavedAnime, "anime"),
    "manga": (Manga, SavedManga, "manga"),
}


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
    is_saved = (
        request.user.is_authenticated
        and SavedMovie.objects.filter(user=request.user, movie=movie).exists()
    )
    return render(
        request, "media/movie/detail.html", {"movie": movie, "is_saved": is_saved}
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


def _resolve(content_type: str) -> tuple[type[Model], type[Model], str]:
    """Translate a content-type slug into (content_model, saved_model, fk_name)."""
    if content_type not in CONTENT_TYPE_MAP:
        raise Http404(f"Unknown content type: {content_type}")
    return CONTENT_TYPE_MAP[content_type]


def _safe_redirect(request: HttpRequest, fallback: str = "media:home") -> HttpResponse:
    """Redirect to ?next= if it's a safe local URL, otherwise to fallback."""
    next_url = request.POST.get("next")
    if next_url and url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}
    ):
        return redirect(next_url)
    return redirect(fallback)


@login_required  # type: ignore
@require_POST  # type: ignore
def save_item(request: HttpRequest, content_type: str, object_id: int) -> HttpResponse:
    content_model, saved_model, fk_name = _resolve(content_type)
    item = get_object_or_404(content_model, pk=object_id)
    lookup: dict[str, Any] = {"user": request.user, fk_name: item}
    saved_model.objects.get_or_create(**lookup)
    return _safe_redirect(request)


@login_required  # type: ignore
@require_POST  # type: ignore
def unsave_item(
    request: HttpRequest, content_type: str, object_id: int
) -> HttpResponse:
    content_model, saved_model, fk_name = _resolve(content_type)
    item = get_object_or_404(content_model, pk=object_id)
    lookup: dict[str, Any] = {"user": request.user, fk_name: item}
    saved_model.objects.filter(**lookup).delete()
    return _safe_redirect(request)
