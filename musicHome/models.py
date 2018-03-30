from django.db import models

# Create your models here.


class Artist(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="artist_image")

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
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    title = models.CharField(max_length=250)
    song_logo = models.ImageField(upload_to="song_logo",default="")
    file = models.FileField(upload_to="album_song")
    upcoming = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title}"
