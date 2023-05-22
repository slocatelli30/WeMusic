# import forms
from django import forms
# import Playlist
from .models import Playlist

class AllSearchForm(forms.Form):
    q = forms.CharField(label="", widget=forms.TextInput(attrs={'class': 'form-control me-2'}))

class CreatePlaylistForm(forms.Form):
    playlist_name = forms.CharField(
        label='Crea nuova playlist:', 
        widget=forms.TextInput(attrs={'class': 'form-control mb-3'})
    )

class AddSongToPlaylistForm(forms.Form):
    playlist = forms.ModelChoiceField(
        queryset=Playlist.objects.all(), 
        empty_label="---",
        widget=forms.Select(attrs={'class': 'form-control mb-3'})
    )

# ricerca utente (OrdinaryUser)
class SearchOrdinaryUserForm(forms.Form):
    q = forms.CharField(label='Cerca un utente:')
