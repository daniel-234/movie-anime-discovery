from django.shortcuts import render

from .tmdb import get_movie_list_from_api


def movie_list(request):
    movies = get_movie_list_from_api("/trending/movie/week")
    return render(request, "media/movie/list.html", {"movies": movies})
