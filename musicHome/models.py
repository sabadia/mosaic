from django.db import models
from django.contrib.auth.models import Permission, User
from django.urls import reverse

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="artist_image")
    detail = models.TextField(default="")

    def __str__(self):
        return self.name


class Album(models.Model):
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    year = models.DateField()
    album_logo = models.ImageField(upload_to="album_logo")

    def __str__(self):
        return f"{self.title}"


class Song(models.Model):
    uploaded_by = models.ForeignKey(User,default=1, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    song_logo = models.ImageField(upload_to="song_logo", default="")
    file = models.FileField(upload_to="album_song")
    gnere = models.CharField(max_length=50, default="")

    def __str__(self):
        return f"{self.title}"


class Favourite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.song.title} favourite by {self.user.username}"
