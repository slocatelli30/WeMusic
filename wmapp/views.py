from .decorators import require_ordinary_user, require_artist, derive_user_type
from django.contrib.auth.decorators import login_required
from django.core import serializers
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from .models import Playlist, OrdinaryUser, Song, Artist, Album, Account
from .forms import AllSearchForm, CreatePlaylistForm, AddSongToPlaylistForm
import collections
import json
import datetime
from django.contrib.auth.models import User
# import (machine learning)
from pandas import read_csv
from sklearn.tree import DecisionTreeClassifier
# import Q
from django.db.models import Q

@derive_user_type
def index(request):
    """View function for home page of site."""

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
            # nome dell'utente corrente
            'name': ordinary_user.account.name,
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
        'album': album,
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
    # oggetto account
    account = request.account

    # context
    context = {
        'name': account.name,
        'surname': account.surname,
        'email': account.email,
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

# view per la pagina social (principale)
@login_required
@derive_user_type
@require_ordinary_user
def people(request):
    """View function for social"""

    if request.method == 'GET':
        form = AllSearchForm()
    else:
        form = AllSearchForm(request.POST)

    # context
    context = {
        'form': form
    }

    return render(request, 'people_results.html', context)

# view per la ricerca di utenti
@login_required
@derive_user_type
@require_ordinary_user
def people_results(request):
    if request.method == 'GET':
        ordinaryuser = []
        form = AllSearchForm()
    else:
        form = AllSearchForm(request.POST)
        # filtro tutti gli utenti presenti nel db per parte del nome
        #ordinaryuser = OrdinaryUser.objects.filter(account__name__icontains=form.data['q'])
        ordinaryuser = OrdinaryUser.objects.filter( Q(account__name__icontains=form.data['q']) | 
                                                   Q(account__surname__icontains=form.data['q']) )
    
    # ottengo l'utente corrente (ordinaryuser)
    ordinaryuser_current = OrdinaryUser.objects.get(account=request.account)

    # context
    context = {
        'form': form,
        'ordinaryuser': ordinaryuser,
        'ordinaryuser_current_list_friends': ordinaryuser_current.friends.all(),
    }
    return render(request, 'people_results.html', context)

# view per l'aggiunta di amici
@login_required
@derive_user_type
@require_ordinary_user
def add_friends(request, ordinaryuser_id):
    # ottengo l'id dell'utente (ordinaryuser) che voglio aggiungere come amico
    ordinaryuser = get_object_or_404(OrdinaryUser, pk=ordinaryuser_id)
    # ottengo l'utente corrente (ordinaryuser) che vuole aggiungere l'amico
    ordinaryuser_current = OrdinaryUser.objects.get(account=request.account)
    ordinaryuser_current.friends.add(ordinaryuser)
    ordinaryuser_current.save()

    # context
    context = { 'friends_list': ordinaryuser_current.friends.all() }
    #return render(request, 'friends_detail.html', context)
    return redirect('friends_detail')

# view per la visualizzazione della lista amici nella pagina friends
@login_required
@derive_user_type
@require_ordinary_user
def friends_detail(request):
    # ottengo l'utente corrente (ordinaryuser)
    ordinaryuser_current = OrdinaryUser.objects.get(account=request.account)
    # ottengo la lista dei soli amici
    friends_list = ordinaryuser_current.friends.all()
    # context
    context = { 'friends_list': friends_list }
    return render(request, 'friends_detail.html', context)

# view per rimozione degli amici nella pagina friends
@login_required
@derive_user_type
@require_ordinary_user
def remove_friends(request, ordinaryuser_id):
    # ottengo l'id dell'utente (ordinaryuser) che voglio rimuovere dalla lista di amici
    ordinaryuser = get_object_or_404(OrdinaryUser, pk=ordinaryuser_id)
    # ottengo l'utente corrente (ordinaryuser) che vuole rimuovere l'amico
    ordinaryuser_current = OrdinaryUser.objects.get(account=request.account)
    ordinaryuser_current.friends.remove(ordinaryuser)
    ordinaryuser_current.save()
    # context
    context = { 'friends_list': ordinaryuser_current.friends.all() }
    #return render(request, 'friends_detail.html', context)
    return redirect('friends_detail')

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

# view contenente l'algoritmo di discover
@login_required
@derive_user_type
def discover(request):
    # oggetto account
    account = request.account

    # ricavo l'età (finta) dell'utente corrente
    ordinaryuser_current_age = 34
    # ricavo il sesso (finto) dell'utente corrente
    # 0 = femmina, 1 = uomo, maschio
    ordinaryuser_current_gender = 1

    # algoritmo di discover
    # lettura del training set
    utenti = read_csv('utenti.csv')
    # colonna/e di input
    # la funzione drop ci restituisce tutte le colonne tranne quella esplicitata tra apici
    X = utenti.drop(columns=['genmusic'])
    # colonne di output
    y = utenti['genmusic']
    # istanziamo il modello
    modello = DecisionTreeClassifier()
    # alleniamo il modello
    modello.fit(X.values, y.values)
    # [sesso dell'utente target, età dell'utente target]
    # 0 = colonna sesso (0=femmina, 1=maschio), 31 = colonna età obiettivo 
    # 1 = colonne sesso (0=femmina, 1=maschio), 16 = colonne età obiettivo
    # previsione dei generi musicali in base all'eta e al sesso dell'utente corrente
    previsione = modello.predict([[ordinaryuser_current_gender,ordinaryuser_current_age]])
    # salvo il genere musicale dedotto dall'algoritmo
    genere_target = previsione[0]

    # PRIMA PARTE DELL'ALGORITMO DI DISCOVER
    # suggerimento all'utente corrente di vari brani ricavandoli da un dataset.
    # l'algoritmo estrapola per sesso ed età dell'utente corrente i generi musicali
    # suggerendoli mediante una lista di brani
    # estraggo dal db tutti i brani con il genere dedotto dall'algoritmo
    list_songs_genere_target = Song.objects.filter( genre__icontains=genere_target )

    # SECONDA PARTE DELL'ALGORITMO DI DISCOVER
    # creazione della lista vuota contenente gli amici suggeriti dall'algoritmo.
    # criterio: se ad un utente piace almeno un brano con il medesimo genere_target, 
    # viene aggiunto alla lista. Inizialmente la lista degli amici suggeriti è vuota
    list_suggested_friends = []

    # ottengo l'utente corrente (ordinaryuser)
    ordinaryuser_current = OrdinaryUser.objects.get(account=request.account)
    # ottengo gli amici dell'utente corrente
    ordinaryuser_current_friends = ordinaryuser_current.friends.values()

    # in list_friends_accountid estrapolo gli id degli amici dell'utente corrente
    # inizialmente list_friends_accountid è vuota
    list_friends_accountid = []
    for v in ordinaryuser_current_friends:
        list_friends_accountid.append(v["account_id"])

    # primo foreach: sfoglio tutti gli utenti presenti nel db
    for x in OrdinaryUser.objects.all():
        # secondo foreach: sfoglio le canzoni preferite di tutti gli utenti nel db
        for y in x.liked_songs.all().values():
            # salvo il genere musicale in genere_canzone_utente_temp
            genere_canzone_utente_temp = y["genre"]
            
            # condizioni per rientrare tra gli utenti suggeriti:
            # 1) all'utente x del foreach deve piacere almeno una canzone con 
            # lo stesso genere_target che stiamo cercando, allora lo aggiunge 
            # alla lista degli amici suggeriti.
            # 2) l'utente x del foreach non deve essere già un amico dell'utente
            # corrente, ovvero su colui che sta girando l'algoritmo
            # 3) l'utente x del foreach non deve essere lo stesso su cui stiamo
            # eseguendo l'algoritmo
            if ( (genere_target == genere_canzone_utente_temp) and 
            (x.account.id not in list_friends_accountid) and 
            (x.account.id != account.id) ):
                list_suggested_friends.append(x)

    # context
    context = {
        'previsione': previsione,
        'list_songs_genere_target': list_songs_genere_target,
        'list_suggested_friends': list_suggested_friends,
    }
    return render(request, 'discover.html', context)
