from django.contrib import admin

from .models import Anime, Manga, Movie, MovieGenre, SavedAnime, SavedManga, SavedMovie


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


@admin.register(SavedMovie)
class SavedMovieAdmin(admin.ModelAdmin):
    list_display = ("user", "movie", "created")
    list_filter = ("created",)
    search_fields = ("user__username", "movie__title")
    autocomplete_fields = ("user", "movie")


@admin.register(SavedAnime)
class SavedAnimeAdmin(admin.ModelAdmin):
    list_display = ("user", "anime", "created")
    list_filter = ("created",)
    search_fields = ("user__username", "anime__title")
    autocomplete_fields = ("user", "anime")


@admin.register(SavedManga)
class SavedMangaAdmin(admin.ModelAdmin):
    list_display = ("user", "manga", "created")
    list_filter = ("created",)
    search_fields = ("user__username", "manga__title")
    autocomplete_fields = ("user", "manga")
