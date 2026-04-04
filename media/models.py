from django.db import models


class Movie(models.Model):
    adult = models.BooleanField
    backdrop_path = models.CharField(max_length=50)
    id = models.IntegerField
    title = models.CharField(max_length=50)
    original_title = models.CharField(max_length=50)
    overview = models.CharField(max_length=250)
    poster_path = models.CharField(max_length=250)
    media_type = models.CharField(max_length=20)
    original_language = models.CharField(max_length=20)
    genre_ids = models.JSONField(default=list)
    popularity = models.IntegerField
    release_date = models.CharField(max_length=250)
    video = models.BooleanField
    vote_average = models.IntegerField
    vote_count = models.IntegerField
