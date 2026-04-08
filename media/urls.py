from django.urls import path

from . import views

app_name = "media"

urlpatterns = [
    # movie views
    path("", views.movie_list, name="movie_list")
]
