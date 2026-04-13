from django.db import models


class MovieGenre(models.Model):
    name = models.CharField(max_length=100, unique=True)
    genre_id = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.genre_id}: {self.name}"


class AnimeGenre(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name} Anime Genre"


class Movie(models.Model):
    movie_id = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=100)
    overview = models.CharField(max_length=250)
    poster_path = models.URLField(blank=True, null=True)
    backdrop_path = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=20)
    # TODO Check if there's any specification in the API docs about this value length
    original_language = models.CharField(max_length=3)
    genre_ids = models.ManyToManyField(MovieGenre)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    release_date = models.DateField(null=True, blank=True)
    vote_average = models.FloatField(default=0, null=True, blank=True)
    vote_count = models.IntegerField(default=0, null=True, blank=True)
    adult = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Anime(models.Model):
    media_id = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=100)
    genres = models.ManyToManyField(AnimeGenre)
    averageScore = models.IntegerField(default=0, null=True, blank=True)
    # TODO Check if there's any specification in the API docs about this value length
    country_of_origin = models.CharField(max_length=3)
    # TODO Check the documentation to see if there are only a defined set of values
    # so that we can consider it an ENUM type
    status = models.CharField(max_length=50)
    episodes = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.title
