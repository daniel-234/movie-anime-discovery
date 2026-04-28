from django.contrib import admin

from .models import Anime, Manga, Movie, MovieGenre


@admin.register(MovieGenre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ("genre_id", "name")
    search_fields = ("name",)


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ("movie_id", "title", "release_date")
    search_fields = ("title", "overview")
    list_filter = ("release_date",)


@admin.register(Anime)
class AnimeAdmin(admin.ModelAdmin):
    list_display = ("media_id", "title", "country_of_origin")
    search_fields = ("title", "country_of_origin")


@admin.register(Manga)
class MangaAdmin(admin.ModelAdmin):
    list_display = ("media_id", "title", "country_of_origin")
    search_fields = ("title", "country_of_origin")
