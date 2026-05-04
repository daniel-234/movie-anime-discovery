from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    # movie views
    path("", views.home, name="home"),
    path("movie/<slug:movie_slug>/", views.movie_detail, name="movie_detail"),
    path("anime/<slug:anime_slug>/", views.anime_detail, name="anime_detail"),
    path("manga/<slug:manga_slug>/", views.manga_detail, name="manga_detail"),
]
