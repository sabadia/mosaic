from django.urls import path, re_path
from musicHome import views

urlpatterns = [
    path("favourite/", views.favourite, name="favourite"),
    path("search/", views.search, name="search"),
    path("create_album/", views.create_album, name="create_album"),
    path("create_song", views.create_song, name="create_song"),
    re_path("^albums/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/delete_song$", views.delete_song, name="delete_song"),
    path("create_artist", views.create_artist, name="create_artist"),
    path("register/", views.UserFormView.as_view(), name="register"),
    path("login/", views.login,name="login"),
    path("logout/", views.logout_user, name="logout"),
    path("", views.home, name="index"),
    path("artists/", views.radio, name="radio"),
    re_path("artists/(?P<artist_id>[0-9]+)/", views.artist_detail, name="artist_detail"),
    path("albums/", views.browse, name="browse"),
    path("songs/", views.songs, name="songs"),
    path("contact/", views.contact, name="contact"),
    path("error/", views.error, name="error"),
    re_path("^albums/(?P<album_id>[0-9]+)/$", views.album_detail, name="album_detail"),
    re_path("^albums/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/$", views.song_detail, name="song_detail"),
    re_path("^albums/(?P<album_id>[0-9]+)/(?P<song_id>[0-9]+)/f$", views.add_to_favorite, name="add_to_favorite"),


]