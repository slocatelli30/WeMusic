from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('liked_songs', views.liked_songs, name='liked_songs'),
    path('playlists', views.playlists, name='playlists'),
    path('playlists/<int:playlist_id>',
         views.playlist_detail, name='playlist_detail'),
    path('playlists/<int:playlist_id>/remove_song/<int:song_id>',
         views.remove_song_from_playlist, name='remove_song_from_playlist'),
    path('playlist/delete/<int:playlist_id>',
         views.delete_playlist, name='delete_playlist'),
    path('songs/<int:song_id>', views.song_detail, name='song_detail'),
    path('song/like/<int:song_id>', views.like_song, name='like_song'),
    path('song/unlike/<int:song_id>', views.unlike_song, name='unlike_song'),
    path('albums/<int:album_id>', views.album_detail, name='album_detail'),
    path('uploaded_songs', views.uploaded_songs, name='uploaded_songs'),
    path('uploaded_albums', views.uploaded_albums, name='uploaded_albums'),
    path('account_detail', views.account_detail, name='account_detail'),
    path('search/all', views.search_results, name='search_results'),
    path('playlist/create', views.playlist_create, name='playlist_create'),
    path('playlist/addsong/<int:song_id>', views.add_song_to_playlist, name='add_song_to_playlist'),
    path('friends', views.friends, name='friends'),
    path('friends/results', views.friends_search, name='friends_search'),
]
