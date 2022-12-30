from .decorators import require_ordinary_user, require_artist, derive_user_type
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404
from .models import Playlist, OrdinaryUser, Song, Artist, Album, Account
import collections
import json


@derive_user_type
def index(request):
    """View function for home page of site."""

    print(request.user_type)

    if request.user_type is None:
        return render(request, 'index.html')

    # Admin does not have an account
    if request.user_type == 'admin':
        return render(request, 'index.html')

    if request.user_type == 'ordinary':
        ordinary_user = OrdinaryUser.objects.get(account=request.account)

        context = {
            'liked_songs': ordinary_user.liked_songs.order_by('?').all()[:10],
            'playlists': Playlist.objects.filter(creator=ordinary_user).order_by('-creation_date')[:10],
            # 'playlists': ordinary_user.playlist_set.all(),
        }
        return render(request, 'index.html', context)

    if request.user_type == 'artist':
        artist = Artist.objects.get(account=request.account)
        songs = artist.song_set.all()

        seen = collections.OrderedDict()
        for s in songs:
            if s.album.id not in seen:
                seen[s.album.id] = s.album
        albums = list(seen.values())

        context = {
            'songs': songs,
            'albums': albums
        }
        return render(request, 'index.html', context)

    else:
        context = {
            'liked_songs': [],
            'playlists': [], }
        return render(request, 'index.html')


@login_required
@derive_user_type
@require_ordinary_user
def liked_songs(request):
    """View function for liked songs."""

    ordinary_user = OrdinaryUser.objects.get(account=request.account)

    context = {
        'liked_songs_json': json.dumps(list(ordinary_user.liked_songs.order_by('title').all().values())),
    }
    return render(request, 'liked_songs.html', context)


@login_required
@derive_user_type
@require_ordinary_user
def playlists(request):
    """View function for playlists."""

    ordinary_user = OrdinaryUser.objects.get(account=request.account)

    context = {
        'playlists': Playlist.objects.filter(creator=ordinary_user).order_by('name'),
    }
    return render(request, 'playlists.html', context)


@login_required
@derive_user_type
@require_ordinary_user
def playlist_detail(request, playlist_id):
    """View function for playlist detail."""

    playlist = get_object_or_404(Playlist, pk=playlist_id)

    context = {
        'playlist': playlist
    }
    return render(request, 'playlist_detail.html', context)


@derive_user_type
def song_detail(request, song_id):
    """View function for song detail."""

    song = get_object_or_404(Song, pk=song_id)

    context = {
        'song': song
    }
    return render(request, 'song_detail.html', context)


@derive_user_type
def album_detail(request, album_id):
    """View function for album detail."""

    album = get_object_or_404(Album, pk=album_id)

    context = {
        'album': album
    }
    return render(request, 'album_detail.html', context)


@login_required
@derive_user_type
@require_artist
def uploaded_songs(request):
    """View function for uploaded songs."""

    artist = Artist.objects.get(account=request.account)
    uploaded_songs = artist.song_set.all()

    context = {
        'uploaded_songs': uploaded_songs,
    }
    return render(request, 'uploaded_songs.html', context)


@login_required
@derive_user_type
@require_artist
def uploaded_albums(request):
    """View function for uploaded albums."""

    artist = Artist.objects.get(account=request.account)
    songs = artist.song_set.all()

    seen = collections.OrderedDict()
    for s in songs:
        if s.album.id not in seen:
            seen[s.album.id] = s.album
    albums = list(seen.values())

    context = {
        'albums': albums
    }
    return render(request, 'uploaded_albums.html', context)


@login_required
@derive_user_type
def account_detail(request):
    account = request.account

    context = {
        'name': account.name,
        'surname': account.surname,
        'email': account.email,

    }
    return render(request, 'account_detail.html', context)
