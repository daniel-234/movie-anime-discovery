from django.contrib import admin

from .models import Movie, MovieGenre


@admin.register(MovieGenre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre_id", "name")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("movie_id", "title", "release_date")
    search_fields = ("title", "overview")
    list_filter = ("release_date",)
