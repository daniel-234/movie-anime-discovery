from django.contrib import admin

from .models import SavedAnime, SavedManga, SavedMovie


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
    search_fields = ("user__username", "movie__title")
    autocomplete_fields = ("user", "anime")


@admin.register(SavedManga)
class SavedMangaAdmin(admin.ModelAdmin):
    list_display = ("user", "manga", "created")
    list_filter = ("created",)
    search_fields = ("user__username", "mvie__title")
    autocomplete_fields = ("user", "manga")
