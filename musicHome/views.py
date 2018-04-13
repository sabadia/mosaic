from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.db import connection
from .models import Album, Song, Artist, Favourite
from django.contrib.auth import authenticate, login as user_login, logout
from django.views.generic import View
from .forms import UserForm, AlbumForm, SongForm, ArtistForm

# Create your views here.
log = "logout"


def logout_user(request):
    log = ""
    logout(request)
    form = UserForm(request.POST or None)
    context = {
        "form": form, "log": log
    }
    return render(request, 'musicHome/login.html', context)


def login(request):
    log = ""
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                user_login(request, user)
                return redirect("index")
            else:
                return render(request, 'musicHome/login.html', {'error_message': 'Your account has been disabled', "log": log})
        else:
            return render(request, 'musicHome/login.html', {'error_message': 'Invalid login', "log": log})
    return render(request, 'musicHome/login.html', { "log": log})


class UserFormView(View):
    form_class = UserForm
    template_name = "musicHome/registration.html"

    def get(self, request):
        form = self.form_class(None)
        return render(request, self.template_name, {"form": form})

    def post(self, request):
        form = self.form_class(request.POST)

        if form.is_valid():
            user = form.save(commit=False)
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user.set_password(password)
            user.save()

            user = authenticate(username=username, password=password)

            if user is not None:
                if user.is_active:
                    user_login(request, user)
                    return redirect("index")

        return render(request, self.template_name, {"form": form, "log": log})


def home(request):
    username = request.user.username
    if request.user.is_authenticated:
        all_albums = Album.objects.all().order_by("year").reverse()
        albums = zip(range(8), all_albums)
        songs = zip(range(3), Song.objects.all().order_by("album__year").reverse())
        own = Favourite.objects.filter(user=request.user)
        others = Song.objects.exclude(id__in=own.values("song__id"))

        s = others.filter(
            gnere__in=own.values("song__gnere").distinct(),
            album__artist__name__in=own.values("song__album__artist__name").distinct()
        )

        context = {"albums": albums, "all_albums": all_albums, "songs": songs, "username": username, "log": log, "sr": s}
        return render(request, 'musicHome/index.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


@csrf_exempt
def search(request):
    username = request.user.username
    if request.user.is_authenticated:
        query = request.GET.get("search")
        if query:
            albums = Album.objects.all()
            songs = Song.objects.all()
            artists = Artist.objects.all()
            albums = albums.filter(
                Q(title__icontains=query)
            ).distinct()
            artists = artists.filter(
                Q(name__icontains=query)
            )
            songs = songs.filter(
                Q(title__icontains=query)
            )
            context = {"albums": albums, "artists": artists, "songs": songs}
            return render(request, 'musicHome/search.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def browse(request):
    username = request.user.username
    if request.user.is_authenticated:
        albums = Album.objects.all()
        context = {"albums": albums, "username": username, "log": log}
        return render(request, 'musicHome/browse.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def album_detail(request, album_id):
    username = request.user.username
    if request.user.is_authenticated:
        album = Album.objects.get(pk=album_id)
        artist = Artist.objects.get(pk=album.artist_id)
        songs = album.song_set.all()
        context = {"album": album, "artist": artist, "songs": songs, "username": username, "log": log}
        return render(request, 'musicHome/album_detail.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def songs(request):
    username = request.user.username
    if request.user.is_authenticated:
        albums = Album.objects.all()
        context = {"albums": albums, "username": username, "log": log}
        return render(request, 'musicHome/songs.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def song_detail(request, album_id, song_id):
    username = request.user.username
    if request.user.is_authenticated:
        album = Album.objects.get(pk=album_id)
        song = album.song_set.get(pk=song_id)
        songs = album.song_set.all()
        f = Favourite.objects.filter(song__id=song_id, user=request.user).exists()
        context = {"album": album, "song": song, "songs": songs, "username": username, "log": log, "f": f}
        return render(request, 'musicHome/song_detail.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def contact(request):
    username = request.user.username
    if request.user.is_authenticated:
        context = {"username": username, "log": log}
        return render(request, 'musicHome/contact.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def radio(request):
    username = request.user.username
    if request.user.is_authenticated:
        artists = Artist.objects.all()
        context = {"artists": artists, "username": username, "log": log}
        return render(request, 'musicHome/radio.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def artist_detail(request, artist_id):
    username = request.user.username
    if request.user.is_authenticated:
        artist = Artist.objects.all().get(pk=artist_id)
        albums = artist.album_set.all()
        context = {'artist': artist, "albums": albums, "username": username, "log": log}
        return render(request, 'musicHome/artist_detail.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def error(request):
    username = request.user.username
    if request.user.is_authenticated:
        context = {"username": username, "log": log}
        return render(request, 'musicHome/404.html', context)
    return render(request, 'musicHome/login.html', {'error_message': 'Please login first'})


def create_album(request):
    username = request.user.username
    if not request.user.is_authenticated:
        return render(request, 'musicHome/login.html')
    else:
        form = AlbumForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            album = form.save(commit=False)
            album.album_logo = request.FILES['album_logo']
            album.save()
            return redirect("create_song")
        context = {
            "username": username,
            "log": log,
            "form": form,
        }
        return render(request, 'musicHome/create_album.html', context)


def create_song(request):
    username = request.user.username
    if not request.user.is_authenticated:
        return render(request, 'musicHome/login.html')

    form = SongForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        song = form.save(commit=False)
        song.uploaded_by = request.user
        song.save()
        return redirect("create_song")
    else:
        context = {
            "username": username,
            "log": log,
            'form': form,
        }
        return render(request, 'musicHome/create_song.html', context)


def create_artist(request):
    username = request.user.username
    if not request.user.is_authenticated:
        return render(request, 'musicHome/login.html')

    form = ArtistForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        artist = form.save(commit=False)
        artist.save()
        form = AlbumForm(request.POST or None, request.FILES or None)
        return redirect("create_album")
    else:
        context = {
            "username": username,
            "log": log,
            'form': form,
        }
        return render(request, 'musicHome/create_artist.html', context)


def delete_song(request, album_id, song_id):
    if not request.user.is_authenticated:
        return render(request, 'musicHome/login.html')
    song = Song.objects.get(pk=song_id)
    if song.uploaded_by == request.user:
        song.delete()
        return redirect("album_detail", album_id)
    return redirect("song_detail", album_id, song_id)


def favourite(request):
    username = request.user.username
    if not request.user.is_authenticated:
        return render(request, 'musicHome/login.html')
    user = request.user
    fav = list(user.favourite_set.only("song"))
    print(fav)
    context = {
        "albums": Album.objects.all(),
        "username": username,
        "log": log,
        "fav": fav,
    }
    return render(request, "musicHome/favourite.html", context)


def add_to_favorite(request, album_id, song_id):
    song = get_object_or_404(Song, pk=song_id)
    s = Favourite.objects.filter(song__id=song_id, user=request.user).exists()

    if not s:
        s = Favourite(user=request.user, song=Song.objects.get(id=song_id))
        s.save()
        return redirect("song_detail", album_id, song_id)
    else:
        s = Favourite.objects.filter(song__id=song_id, user=request.user)
        s.delete()
        return redirect("song_detail", album_id, song_id)
