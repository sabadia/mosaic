from django.urls import path, re_path
from musicHome import views

urlpatterns = [
    path("", views.home, name="index"),
    path("artists/", views.radio, name="radio"),
    re_path("artists/(?P<artist_id>[0-9]+)/", views.artist_detail, name="artist_detail"),
    path("albums/", views.browse, name="browse"),
    path("songs/", views.songs, name="songs"),
    path("contact/", views.contact, name="contact"),
    path("error/", views.error, name="error"),
    re_path("^albums/(?P<album_id>[0-9]+)/$", views.album_detail, name="album_detail"),
    re_path("^albums/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/$", views.song_detail, name="song_detail"),

]