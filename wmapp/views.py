import random
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Playlist, OrdinaryUser, Account


def require_ordinary_user(fun):
    def wrapper(request):
        if request.user_type == 'ordinary':
            return fun(request)
        return redirect('index')
    return wrapper


def derive_user_type(fun):
    def wrapper(request):

        if not request.user.is_authenticated:
            request.user_type = None
            return fun(request)

        if not Account.objects.filter(user=request.user).exists():
            request.user_type = 'admin'
            return fun(request)

        request.account = Account.objects.get(user=request.user)

        if OrdinaryUser.objects.filter(account=request.account).exists():

            request.user_type = 'ordinary'
        else:
            request.user_type = 'artist'

        return fun(request)
    return wrapper


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
