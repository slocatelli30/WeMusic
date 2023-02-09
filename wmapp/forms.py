from django import forms


class AllSearchForm(forms.Form):
    q = forms.CharField(label='Cerca:')


class CreatePlaylistForm(forms.Form):
    playlist_name = forms.CharField(label='Crea nuova playlist:')
