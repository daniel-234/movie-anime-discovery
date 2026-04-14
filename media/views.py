from django.shortcuts import get_object_or_404, render

from .models import Anime, Movie


def home(request):
    context = {
        "movie_list": Movie.objects.all()[:5],
        "anime_list": Anime.objects.all()[:5],
    }

    return render(request, "media/home.html", context)


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "media/movie/detail.html", {"movie": movie})


def anime_detail(request, id):
    anime = get_object_or_404(Anime, id=id)
    return render(request, "media/anime/detail.html", {"anime": anime})
