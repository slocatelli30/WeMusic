from django import forms


class SongSearchForm(forms.Form):
    q = forms.CharField(label='Cerca:')
