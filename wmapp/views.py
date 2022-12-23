from django.shortcuts import render
from django.http import HttpRequest, HttpResponse


def index(request):
    """View function for home page of site."""

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html')
