import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Playlist, OrdinaryUser, Account


def require_ordinary_user(fun):

    def wrapper(request):
        # If admin without account, dont crash
        if not Account.objects.filter(user=request.user).exists():
            return redirect('index')

        account = Account.objects.get(user=request.user)

        if OrdinaryUser.objects.filter(account=account).exists():
            ordinary_user = OrdinaryUser.objects.get(account=account)

            return fun(request, ordinary_user)
        else:
            return redirect('index')

    return wrapper


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


@login_required
@require_ordinary_user
def liked_songs(request, ordinary_user):
    """View function for liked songs."""
    context = {
        'liked_songs': ordinary_user.liked_songs.order_by('title').all(),
    }
    return render(request, 'liked_songs.html', context)


@login_required
@require_ordinary_user
def playlists(request, ordinary_user):
    """View function for playlists."""

    context = {
        'playlists': Playlist.objects.filter(creator=ordinary_user).order_by('name'),
    }
    return render(request, 'playlists.html', context)
