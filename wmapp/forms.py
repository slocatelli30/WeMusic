from django import forms
from .models import Playlist


class AllSearchForm(forms.Form):
    q = forms.CharField(label='Cerca:')

class CreatePlaylistForm(forms.Form):
    playlist_name = forms.CharField(label='Crea nuova playlist:')

class AddSongToPlaylistForm(forms.Form):
    playlist = forms.ModelChoiceField(
        queryset=Playlist.objects.all(), empty_label="---")

# ricerca utente (OrdinaryUser)
class SearchOrdinaryUserForm(forms.Form):
    q = forms.CharField(label='Cerca un utente:')
