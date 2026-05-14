from django.conf import settings
from django.db import models
from django.templatetags.static import static
from django.utils.text import slugify


class MovieGenre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.genre_id}: {self.name} Movie Genre"


class AnimeGenre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} Anime Genre"


class Movie(models.Model):
    movie_id = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    overview = models.TextField(blank=True)
    poster_path = models.CharField(max_length=200, blank=True)
    backdrop_path = models.CharField(max_length=200, blank=True)
    media_type = models.CharField(max_length=20)
    # TODO Check if there's any specification in the API docs about this value length
    original_language = models.CharField(max_length=3)
    genre_ids = models.ManyToManyField(MovieGenre)
    popularity = models.FloatField(default=0, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(default=0, null=True, blank=True)
    vote_count = models.IntegerField(default=0, null=True, blank=True)
    adult = models.BooleanField(default=False)

    @property
    def year(self):
        """Year for display, derived from release_date. Mirrors the
        `year` integer field on Anime/Manga so templates can treat all
        three content types uniformly via `item.year`."""
        return self.release_date.year if self.release_date else None

    def __str__(self):
        return self.title

    def poster_url(self, size="w342"):
        if not self.poster_path:
            return static("media/placeholder-poster.png")
        return f"{settings.TMDB_IMAGE_BASE}/{size}{self.poster_path}"

    def backdrop_url(self, size="w780"):
        if not self.backdrop_path:
            return ""
        return f"{settings.TMDB_IMAGE_BASE}/{size}{self.backdrop_path}"

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Movie.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Anime(models.Model):
    media_id = models.IntegerField(default=0, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    title_english = models.CharField(max_length=100, null=True, blank=True)
    title_romaji = models.CharField(max_length=100, null=True, blank=True)
    title_native = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    genres = models.ManyToManyField(AnimeGenre)
    cover_image = models.URLField(blank=True, null=True)
    # TODO `score` (Anime/Manga, IntegerField) and `Movie.vote_average`
    # (FloatField) are the same concept with different names and types.
    # Unify when convenient — note it touches the model, the sync
    # command, and every template/view that references either field.
    score = models.IntegerField(default=0, null=True, blank=True)
    # TODO Check if there's any specification in the API docs about this value length
    country_of_origin = models.CharField(max_length=3)
    # TODO Check the documentation to see if there are only a defined set of values
    # so that we can consider it an ENUM type
    status = models.CharField(max_length=50)
    episodes = models.IntegerField(default=0, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    # TODO Like `status`, AniList's format is a fixed set of values —
    # consider converting both to TextChoices enums together later.
    format = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Anime.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


class Manga(models.Model):
    media_id = models.IntegerField(default=0, unique=True, blank=True, null=True)
    title = models.CharField(max_length=100)
    title_english = models.CharField(max_length=100, null=True, blank=True)
    title_romaji = models.CharField(max_length=100, null=True, blank=True)
    title_native = models.CharField(max_length=100, null=True, blank=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True, null=True)
    genres = models.ManyToManyField(AnimeGenre)
    cover_image = models.URLField(blank=True, null=True)
    score = models.IntegerField(default=0, null=True, blank=True)
    # TODO Check if there's any specification in the API docs about this value length
    country_of_origin = models.CharField(max_length=3)
    # TODO Check the documentation to see if there are only a defined set of values
    # so that we can consider it an ENUM type
    status = models.CharField(max_length=50)
    chapters = models.IntegerField(default=0, null=True, blank=True)
    volumes = models.IntegerField(default=0, null=True, blank=True)
    year = models.IntegerField(null=True, blank=True)
    # TODO Like `status`, AniList's format is a fixed set of values —
    # consider converting both to TextChoices enums together later.
    format = models.CharField(max_length=20, blank=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1

            while Manga.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)


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


class Service(models.Model):
    """A streaming/rental/purchase service (Netflix, Disney+, etc.).

    Populated from TMDB's /watch/providers/movie endpoint. Provider data
    originates from JustWatch — attribution required when displaying.
    """

    tmdb_provider_id = models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    logo_path = models.CharField(max_length=200, blank=True)
    display_priority = models.IntegerField(default=0)

    class Meta:
        ordering = ["display_priority", "name"]

    def __str__(self):
        return self.name

    def logo_url(self, size="w45"):
        if not self.logo_path:
            return ""
        return f"{settings.TMDB_IMAGE_BASE}/{size}{self.logo_path}"


class StreamingOffer(models.Model):
    class OfferType(models.TextChoices):
        FLATRATE = "flatrate", "Flatrate"
        RENT = "rent", "Rent"
        BUY = "buy", "Buy"
        ADS = "ads", "Free with ads"
        FREE = "free", "Free"

    movie = models.ForeignKey(
        Movie,
        on_delete=models.CASCADE,
        related_name="offers",
    )
    service = models.ForeignKey(
        Service,
        on_delete=models.PROTECT,
        related_name="offers",
    )
    country = models.CharField(max_length=2)
    offer_type = models.CharField(
        max_length=10,
        choices=OfferType.choices,
    )
    fetched_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["movie", "service", "country", "offer_type"],
                name="unique_offer_per_movie_service_country_type",
            ),
        ]
        ordering = ["service__display_priority", "service__name"]

    def __str__(self):
        return f"{self.movie.title} on {self.service.name} ({self.country}, {self.offer_type})"
