from .decorators import require_ordinary_user, require_artist, derive_user_type
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from .models import Playlist, OrdinaryUser, Song, Artist, Album, Account
from .forms import AllSearchForm, CreatePlaylistForm, AddSongToPlaylistForm, SearchFriendsForm
import collections
import json
import datetime
from django.contrib.auth.models import User
# import (machine learning)
from pandas import read_csv
from sklearn.tree import DecisionTreeClassifier

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

# download song
@login_required
@derive_user_type
@require_ordinary_user
def download_song(request):
    downloadsong = Song.objects.all()
    return render(request, 'playlist_detail.html', {'downloadsong':downloadsong})

@login_required
@derive_user_type
@require_ordinary_user
def liked_songs(request):
    """View function for liked songs."""

    ordinary_user = OrdinaryUser.objects.get(account=request.account)

    context = {
        'songs': ordinary_user.liked_songs.order_by('title').all(),
    }
    return render(request, 'liked_songs.html', context)


@login_required
@derive_user_type
@require_ordinary_user
def playlists(request):
    """View function for playlists."""

    ordinary_user = OrdinaryUser.objects.get(account=request.account)
    context = {
        'playlists': Playlist.objects.filter(creator=ordinary_user),
        'form': CreatePlaylistForm(),

    }
    return render(request, 'playlists.html', context)


@login_required
@derive_user_type
@require_ordinary_user
def playlist_detail(request, playlist_id):
    """View function for playlist detail."""

    playlist = get_object_or_404(Playlist, pk=playlist_id)

    context = {
        'songs': playlist.songs.order_by('title').all(),
        'playlist': playlist

    }
    return render(request, 'playlist_detail.html', context)


@login_required
@derive_user_type
def song_detail(request, song_id):
    """View function for song detail."""

    song = get_object_or_404(Song, pk=song_id)

    context = {
        'song': song,
        'form': None,
        'is_liked': False
    }

    if request.user_type == 'ordinary':
        ordinary_user = OrdinaryUser.objects.get(account=request.account)
        context['form'] = AddSongToPlaylistForm()
        context['form'].fields['playlist'].queryset = Playlist.objects.filter(
            creator=ordinary_user)
        if ordinary_user.liked_songs.contains(song):
            context['is_liked'] = True
    return render(request, 'song_detail.html', context)


@derive_user_type
def album_detail(request, album_id):
    """View function for album detail."""

    album = get_object_or_404(Album, pk=album_id)

    context = {
        'songs': album.song_set.order_by('title').all(),
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
        'songs': uploaded_songs.order_by('title').all(),
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
        'albums': albums,
    }
    return render(request, 'uploaded_albums.html', context)


@login_required
@derive_user_type
def account_detail(request):
    account = request.account

    # algoritmo di discover
    # lettura del training set
    utenti = read_csv('utenti.csv')
    # colonne di input
    # la funzione drop ci restituisce tutte le colonne tranne quella esplicitata tra apici
    X = utenti.drop(columns=['genmusic'])
    # colonne di putput
    y = utenti['genmusic']
    # istanziamo il modello
    modello = DecisionTreeClassifier()
    # alleniamo il modello
    modello.fit(X.values, y.values)
    # 0 = colonna sesso (0=femmina, 1=maschio), 31 = colonna età obiettivo 
    # 1 = colonne sesso (0=femmina, 1=maschio), 16 = colonne età obiettivo
    previsione = modello.predict([[0,31], [1,16]])

    context = {
        'name': account.name,
        'surname': account.surname,
        'email': account.email,
        'previsione': previsione,
    }
    return render(request, 'account_detail.html', context)


@login_required
@derive_user_type
def search_results(request):
    if request.method == 'GET':
        songs = []
        albums = []
        form = AllSearchForm()
    else:
        form = AllSearchForm(request.POST)
        songs = Song.objects.filter(title__icontains=form.data['q'])
        albums = Album.objects.filter(name__icontains=form.data['q'])

    context = {
        'form': form,
        'songs': songs,
        'albums': albums,
    }
    return render(request, 'search_results.html', context)

# view per la pagina friends (principale)
@login_required
@derive_user_type
@require_ordinary_user
def friends(request):
    """View function for friends"""

    #ordinary_user = OrdinaryUser.objects.get(account=request.account)

    context = {
        # lista utenti
        'list_user': Account.objects.all(),
    }

    return render(request, 'friends.html', context)

# view per la ricerca di utenti
@login_required
@derive_user_type
@require_ordinary_user
def friends_search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        friends = Account.objects.filter(name__contains=searched)
        return render(request, 'friends_results.html', {'searched': searched, 'friends': friends})
    else:
        return render(request, 'friends_results.html', {})

@login_required
@derive_user_type
@require_ordinary_user
def playlist_create(request):
    form = CreatePlaylistForm(request.POST)
    ordinary_user = OrdinaryUser.objects.get(account=request.account)
    p = Playlist(creator=ordinary_user, name=form.data['playlist_name'])
    p.save()
    return redirect('playlist_detail', playlist_id=p.id)


@login_required
@derive_user_type
@require_ordinary_user
def add_song_to_playlist(request, song_id):
    form = AddSongToPlaylistForm(request.POST)
    song = get_object_or_404(Song, pk=song_id)
    playlist = get_object_or_404(Playlist, pk=form.data['playlist'])
    playlist.songs.add(song)
    playlist.save()
    return redirect('song_detail', song_id=song_id)


@login_required
@derive_user_type
@require_ordinary_user
def like_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    ordinary_user = OrdinaryUser.objects.get(account=request.account)
    ordinary_user.liked_songs.add(song)
    ordinary_user.save()
    return redirect('song_detail', song_id=song_id)


@login_required
@derive_user_type
@require_ordinary_user
def unlike_song(request, song_id):
    song = get_object_or_404(Song, pk=song_id)
    ordinary_user = OrdinaryUser.objects.get(account=request.account)
    ordinary_user.liked_songs.remove(song)
    ordinary_user.save()
    return redirect('song_detail', song_id=song_id)


@login_required
@derive_user_type
@require_ordinary_user
def delete_playlist(request, playlist_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    playlist.delete()
    return redirect('playlists')


@login_required
@derive_user_type
@require_ordinary_user
def remove_song_from_playlist(request, playlist_id, song_id):
    playlist = get_object_or_404(Playlist, pk=playlist_id)
    song = get_object_or_404(Song, pk=song_id)
    playlist.songs.remove(song)
    playlist.save()
    return redirect('playlist_detail', playlist_id=playlist.id)
