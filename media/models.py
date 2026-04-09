from django.db import models


class Movie(models.Model):
    movie_id = models.IntegerField(default=0, unique=True)
    title = models.CharField(max_length=100)
    overview = models.CharField(max_length=250)
    poster_path = models.URLField(blank=True, null=True)
    backdrop_path = models.URLField(blank=True, null=True)
    media_type = models.CharField(max_length=20)
    original_language = models.CharField(max_length=3)
    # TODO Change this to a many-to-many relationship
    genre_ids = models.JSONField(null=True, blank=True)
    popularity = models.IntegerField(default=0, null=True, blank=True)
    release_date = models.CharField(max_length=250)
    vote_average = models.FloatField(default=0, null=True, blank=True)
    vote_count = models.IntegerField(default=0, null=True, blank=True)
    adult = models.BooleanField(default=False)
    # Explicitly declare the manager on the model as it is added
    # dynamically by Django's metaclass and static analysis tools
    # like the "ty" typechecker can't see it, flagging it as missing.
    objects: models.Manager
