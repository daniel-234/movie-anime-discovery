from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    # movie views
    path("", views.home, name="home"),
    path("movies/<int:id>/", views.movie_detail, name="movie_detail"),
    path("anime/<int:id>/", views.anime_detail, name="anime_detail"),
]
