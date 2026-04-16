from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    # movie views
    path("", views.home, name="home"),
    path("movie/<slug:movie>/", views.movie_detail, name="movie_detail"),
    path("anime/<slug:anime>/", views.anime_detail, name="anime_detail"),
]
