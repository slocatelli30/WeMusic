from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from .models import Song, Playlist, OrdinaryUser, Account


def index(request):
    """View function for home page of site."""

    if not request.user.is_authenticated:
        return render(request, 'index.html')

    account = Account.objects.get(user=request.user)

    if OrdinaryUser.objects.filter(account=account).exists():
        ordinary_user = OrdinaryUser.objects.get(account=account)

        context = {
            'liked_songs': ordinary_user.liked_songs.all(),
            'playlists': Playlist.objects.filter(creator=ordinary_user),
            # 'playlists': ordinary_user.playlist_set.all(),
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')
