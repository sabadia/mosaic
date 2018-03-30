from django.shortcuts import render
from django.http import HttpResponse
from .models import Album, Song, Artist
# Create your views here.


def home(request):
    all_albums = Album.objects.all().order_by("year")
    albums = zip(range(12), all_albums)
    songs = zip(range(3), Song.objects.all().order_by("album__year").reverse())
    context = {"albums": albums, "all_albums": all_albums, "songs": songs}
    return render(request, 'musicHome/index.html', context)


def browse(request):
    albums = Album.objects.all()
    context = {"albums": albums}
    return render(request, 'musicHome/browse.html', context)


def album_detail(request, album_id):
    album = Album.objects.get(pk=album_id)
    artist = Artist.objects.get(pk=album.artist_id)
    songs = album.song_set.all()
    context = {"album": album, "artist": artist, "songs": songs}
    return render(request, 'musicHome/album_detail.html', context)


def songs(request):
    albums = Album.objects.all()
    context = {"albums": albums}
    return render(request, 'musicHome/songs.html', context)


def song_detail(request, album_id, song_id):
    album = Album.objects.get(pk=album_id)
    song = album.song_set.get(pk=song_id)
    songs = album.song_set.all()
    context = {"album": album, "song": song, "songs": songs}
    return render(request, 'musicHome/song_detail.html', context)


def contact(request):
    context = {}
    return render(request, 'musicHome/contact.html', context)


def radio(request):
    artists = Artist.objects.all()
    context = {"artists": artists}
    return render(request, 'musicHome/radio.html', context)


def artist_detail(request, artist_id):
    artist = Artist.objects.all().get(pk=artist_id)
    albums = artist.album_set.all()
    context = {'artist': artist, "albums": albums}
    return render(request, 'musicHome/artist_detail.html', context)


def error(request):
    context = {}
    return render(request, 'musicHome/404.html', context)
