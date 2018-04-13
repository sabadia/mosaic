from django.contrib.auth.models import User
from django import forms
from .models import Album, Song, Artist


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email", "password"]


class AlbumForm(forms.ModelForm):

    class Meta:
        model = Album
        fields = ['artist', 'title', 'year', 'album_logo']


class SongForm(forms.ModelForm):

    class Meta:
        model = Song
        fields = ["album", "title", "song_logo", "file", "gnere"]


class ArtistForm(forms.ModelForm):
    class Meta:
        model = Artist
        fields = ["name", "image", "detail"]

