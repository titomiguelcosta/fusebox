from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import localtime
from django.conf import settings


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
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
    url = models.CharField(max_length=250, blank=True, null=True)
    artists = models.ManyToManyField(Artist)
    spotify_id = models.CharField(max_length=250, blank=True, null=True)
    analysis_url = models.CharField(max_length=250, blank=True, null=True)
    key = models.IntegerField(default=0, blank=True, null=True)
    time_signature = models.IntegerField(default=0, blank=True, null=True)
    popularity = models.IntegerField(default=0.0, blank=True, null=True)
    danceability = models.FloatField(default=0.0, blank=True, null=True)
    energy = models.FloatField(default=0.0, blank=True, null=True)
    loudness = models.FloatField(default=0.0, blank=True, null=True)
    speechiness = models.FloatField(default=0.0, blank=True, null=True)
    acousticness = models.FloatField(default=0.0, blank=True, null=True)
    instrumentalness = models.FloatField(default=0.0, blank=True, null=True)
    liveness = models.FloatField(default=0.0, blank=True, null=True)
    valence = models.FloatField(default=0.0, blank=True, null=True)
    tempo = models.FloatField(default=0.0, blank=True, null=True)
    duration_ms = models.FloatField(default=0.0, blank=True, null=True)
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
    tracks = models.ManyToManyField(Track, through='PlaylistTracks')

    def __str__(self):
        return self.name


class PlaylistTracks(models.Model):
    track = models.ForeignKey(Track, related_name='playlist_tracks_track', on_delete=models.CASCADE)
    playlist = models.ForeignKey(Playlist, related_name='playlist_tracks_playlist', on_delete=models.CASCADE)
    queued_by = models.ForeignKey(User, related_name='playlist_tracks_queued_by', null=True, on_delete=models.SET_NULL)
    queued_on = models.DateTimeField()
    dequeued_by = models.ForeignKey(
        User, related_name='playlist_tracks_dequeued_by', null=True, on_delete=models.SET_NULL
    )
    dequeued_on = models.DateTimeField(null=True)

    class Meta:
        verbose_name_plural = "Playlist tracks"

    def __str__(self):
        user_name = self.user().first_name if self.user() else "Unknown"

        return "%s %s on playlist %s by %s" % (
            self.track, self.action(), self.playlist, user_name
        )

    def action(self):
        default = "dequeued"
        if (self.queued_on and not self.dequeued_on) \
                or (self.queued_on and self.dequeued_on and self.queued_on > self.dequeued_on):
            default = "queued"

        return default

    def user(self):
        return self.queued_by if self.action() == "queued" else self.dequeued_by


class Video(models.Model):
    track = models.ForeignKey(Track, related_name='video_tracks_track', on_delete=models.CASCADE)
    source = models.CharField(max_length=255, default='youtube')
    title = models.TextField()
    description = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255, blank=True, null=True)
    video_id = models.CharField(max_length=255)
    channel_id = models.CharField(max_length=255, blank=True, null=True)
    published_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return "%s: %s" % (self.title, self.url)


class Rate(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    score = models.IntegerField()
    category = models.CharField(max_length=250, default="like")
    on = models.DateTimeField()

    def __str__(self):
        return "%s scored %s on track %s by %s" % (
            self.user.first_name, self.score, self.track, self.track.artists_to_str
        )


class Played(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    on = models.DateTimeField()

    def __str__(self):
        return "%s by %s played on %s" % (
            self.track.title, self.track.artists_to_str, localtime(self.on).strftime(settings.DATETIME_FORMAT)
        )

    class Meta:
        verbose_name_plural = "Played"


class Configuration(models.Model):
    name = models.CharField(max_length=250)
    value = models.TextField()

    def __str__(self):
        return self.name
