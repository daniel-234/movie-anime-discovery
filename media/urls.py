from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    # movie views
    path("", views.movie_list, name="movie_list"),
    path("<int:id>/", views.movie_detail, name="movie_detail"),
    path("anime/", views.anime_list, name="anime_list"),
    path("<int:id>/", views.anime_detail, name="anime_detail"),
]
