from django.shortcuts import get_object_or_404, render

from library.models import SavedAnime, SavedManga, SavedMovie

from .models import Anime, Manga, Movie

POSTERS_PER_ROW = 5


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
