from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('liked_songs', views.liked_songs, name='liked_songs'),
    path('playlists', views.playlists, name='playlists'),
    path('playlists/<int:playlist_id>',
         views.playlist_detail, name='playlist_detail'),
    path('songs/<int:song_id>', views.song_detail, name='song_detail'),
    path('albums/<int:album_id>', views.album_detail, name='album_detail'),
    path('uploaded_songs', views.uploaded_songs, name='uploaded_songs'),
    path('uploaded_albums', views.uploaded_albums, name='uploaded_albums'),

]
