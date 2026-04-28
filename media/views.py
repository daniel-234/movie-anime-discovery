from django.shortcuts import get_object_or_404, render

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
    return render(request, "media/movie/detail.html", {"movie": movie})


def anime_detail(request, anime_slug):
    anime = get_object_or_404(Anime, slug=anime_slug)
    return render(request, "media/anime/detail.html", {"anime": anime})


def manga_detail(request, manga_slug):
    manga = get_object_or_404(Manga, slug=manga_slug)
    return render(request, "media/manga/detail.html", {"manga": manga})
