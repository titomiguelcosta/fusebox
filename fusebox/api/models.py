from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    slack_username = models.CharField(max_length=200)
    notifications = models.BooleanField(default=True)

    def __str__(self):
        return "%s's profile" % self.user

    class Meta:
        verbose_name_plural = "User profiles"


class Artist(models.Model):
    name = models.CharField(max_length=250)
    popularity = models.IntegerField(default=0)
    genres = models.CharField(max_length=250, blank=True)
    spotify_id = models.CharField(max_length=250, blank=True)

    def __str__(self):
        return self.name


class Track(models.Model):
    title = models.CharField(max_length=250)
    album = models.CharField(max_length=250, blank=True)
    url = models.CharField(max_length=250, blank=True, null="")
    artists = models.ManyToManyField(Artist)
    spotify_id = models.CharField(max_length=250, blank=True)
    popularity = models.IntegerField(default=0.0)
    danceability = models.FloatField(default=0.0)
    energy = models.FloatField(default=0.0)
    loudness = models.FloatField(default=0.0)
    speechiness = models.FloatField(default=0.0)
    acousticness = models.FloatField(default=0.0)
    instrumentalness = models.FloatField(default=0.0)
    liveness = models.FloatField(default=0.0)
    valence = models.FloatField(default=0.0)
    tempo = models.FloatField(default=0.0)
    duration_ms = models.FloatField(default=0.0)
    populated = models.BooleanField(default=False)

    @property
    def artists_to_str(self):
        artists = [str(artist) for artist in self.artists.all()]

        return 'Unknown' if 0 == len(artists) else ", ".join(artists)

    def __str__(self):
        return self.title


class Playlist(models.Model):
    name = models.CharField(max_length=250)
    description = models.CharField(max_length=250, blank=True)
    spotify_id = models.CharField(max_length=250, blank=True)
    tracks = models.ManyToManyField(Track)

    def __str__(self):
        return self.name


class Rate(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    category = models.CharField(max_length=250, default="like")
    on = models.DateTimeField()

    def __str__(self):
        return "User %s scored %s on track %s" % (self.user, self.score, self.track)


class Played(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    on = models.DateTimeField()


class Configuration(models.Model):
    name = models.CharField(max_length=250)
    value = models.TextField()

    def __str__(self):
        return self.name
