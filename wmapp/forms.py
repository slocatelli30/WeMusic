from django import forms


class AllSearchForm(forms.Form):
    q = forms.CharField(label='Cerca:')
