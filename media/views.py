from django.shortcuts import get_object_or_404, render

from .models import Movie
from .tmdb import get_movie_list_from_api


def movie_list(request):
    movies = get_movie_list_from_api("/trending/movie/week")
    return render(request, "media/movie/list.html", {"movies": movies})


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "media/movie/detail.html", {"movie": movie})
