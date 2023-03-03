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
    # people
    path('people', views.people, name='people'),
    path('people/all', views.people_results, name='people_results'),
    path('people/add/<int:ordinaryuser_id>', views.add_friends, name='add_friends'),
    # amici
    path('friends', views.friends_detail, name='friends_detail'),
    path('friends/remove/<int:ordinaryuser_id>', views.remove_friends, name='remove_friends'),
]
