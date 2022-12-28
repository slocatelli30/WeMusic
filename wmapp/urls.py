from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('liked_songs', views.liked_songs, name='liked_songs'),
    path('playlists', views.playlists, name='playlists'),

]
