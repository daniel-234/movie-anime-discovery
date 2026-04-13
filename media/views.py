from django.shortcuts import get_object_or_404, render

from .models import Anime, Movie


def movie_list(request):
    movies = Movie.objects.all()[:5]
    return render(request, "media/movie/list.html", {"movies": movies})


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "media/movie/detail.html", {"movie": movie})


def anime_list(request):
    anime = Anime.objects.all()[:5]
    return render(request, "media/anime/list.html", {"anime_list": anime})


def anime_detail(request, id):
    anime = get_object_or_404(Anime, id=id)
    return render(request, "media/anime/detail.html", {"anime": anime})
