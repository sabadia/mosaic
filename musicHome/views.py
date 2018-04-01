from django.db.models import Q
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect, csrf_exempt

from .models import Album, Song, Artist
from django.contrib.auth import authenticate, login as user_login, logout
from django.views.generic import View
from .forms import UserForm

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
        all_albums = Album.objects.all().order_by("year")
        albums = zip(range(12), all_albums)
        songs = zip(range(3), Song.objects.all().order_by("album__year").reverse())
        context = {"albums": albums, "all_albums": all_albums, "songs": songs, "username": username, "log": log}
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
        context = {"album": album, "song": song, "songs": songs, "username": username, "log": log}
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
