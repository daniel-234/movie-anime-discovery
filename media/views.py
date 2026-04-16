from django.shortcuts import get_object_or_404, render

from .models import Anime, Movie

POSTERS_PER_ROW = 5


def home(request):
    context = {
        "movie_list": Movie.objects.all()[:POSTERS_PER_ROW],
        "anime_list": Anime.objects.all()[:POSTERS_PER_ROW],
        "grid_cols_class": f"grid-cols-{POSTERS_PER_ROW}",
    }

    return render(request, "media/home.html", context)


def movie_detail(request, movie):
    movie = get_object_or_404(Movie, slug=movie)
    return render(request, "media/movie/detail.html", {"movie": movie})


def anime_detail(request, anime):
    anime = get_object_or_404(Anime, slug=anime)
    return render(request, "media/anime/detail.html", {"anime": anime})
