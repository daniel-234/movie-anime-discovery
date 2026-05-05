from django.conf import settings
from django.db import models


class SavedMovie(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_movies"
    )
    movie = models.ForeignKey(
        "media.Movie", on_delete=models.CASCADE, related_name="saves"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "movie"], name="unique_user_movie_save"
            )
        ]
        ordering = ["-created"]
        indexes = [models.Index(fields=["user", "-created"])]

    def __str__(self):
        return f"{self.user} saved {self.movie}"


class SavedAnime(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_anime"
    )
    anime = models.ForeignKey(
        "media.Anime", on_delete=models.CASCADE, related_name="saves"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "anime"], name="unique_user_anime_save"
            )
        ]
        ordering = ["-created"]
        indexes = [models.Index(fields=["user", "-created"])]

    def __str__(self):
        return f"{self.user} saved {self.anime}"


class SavedManga(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="saved_manga"
    )
    manga = models.ForeignKey(
        "media.Manga", on_delete=models.CASCADE, related_name="saves"
    )
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "manga"], name="unique_user_manga_save"
            )
        ]
        ordering = ["-created"]
        indexes = [models.Index(fields=["user", "-created"])]

    def __str__(self):
        return f"{self.user} saved {self.manga}"
