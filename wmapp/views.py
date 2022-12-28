import random
from django.shortcuts import render, redirect
from .models import Playlist, OrdinaryUser, Account


def index(request):
    """View function for home page of site."""

    if not request.user.is_authenticated:
        return render(request, 'index.html')

    # If admin without account, dont crash
    if not Account.objects.filter(user=request.user).exists():
        return render(request, 'index.html')

    account = Account.objects.get(user=request.user)

    if OrdinaryUser.objects.filter(account=account).exists():
        ordinary_user = OrdinaryUser.objects.get(account=account)

        context = {
            'liked_songs': ordinary_user.liked_songs.order_by('?').all()[:10],
            'playlists': Playlist.objects.filter(creator=ordinary_user).order_by('-creation_date')[:10],
            # 'playlists': ordinary_user.playlist_set.all(),
        }
        return render(request, 'index.html', context)
    else:
        return render(request, 'index.html')


def liked_songs(request):
    """View function for liked songs."""

    if not request.user.is_authenticated:
        return redirect('index')

    # If admin without account, dont crash
    if not Account.objects.filter(user=request.user).exists():
        return redirect('index')

    account = Account.objects.get(user=request.user)

    if OrdinaryUser.objects.filter(account=account).exists():
        ordinary_user = OrdinaryUser.objects.get(account=account)

        context = {
            'liked_songs': ordinary_user.liked_songs.order_by('title').all(),
        }
        return render(request, 'liked_songs.html', context)
    else:
        return redirect('index')
