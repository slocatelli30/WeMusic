from .decorators import require_ordinary_user, derive_user_type
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from .models import Playlist, OrdinaryUser, Song


@derive_user_type
def index(request):
    """View function for home page of site."""

    print(request.user_type)

    if request.user_type is None:
        return render(request, 'index.html')

    # If admin without account, dont crash
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
        'liked_songs': ordinary_user.liked_songs.order_by('title').all(),
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
