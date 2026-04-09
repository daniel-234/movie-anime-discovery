from django.shortcuts import get_object_or_404, render

from .models import Movie
from .tasks import get_movies, sync_trending_movies


def movie_list(request):
    sync_trending_movies()
    movies = get_movies()
    return render(request, "media/movie/list.html", {"movies": movies})


def movie_detail(request, id):
    movie = get_object_or_404(Movie, id=id)
    return render(request, "media/movie/detail.html", {"movie": movie})
