
from django.shortcuts import redirect
from .models import OrdinaryUser, Account


def require_ordinary_user(fun):
    """
    require_ordinary_user
    """
    def wrapper(request, *args, **kwargs):
        if request.user_type == 'ordinary':
            return fun(request, *args, **kwargs)
        return redirect('index')
    return wrapper


def require_artist(fun):
    """
    require_artist
    """
    def wrapper(request, *args, **kwargs):
        if request.user_type == 'artist':
            return fun(request, *args, **kwargs)
        return redirect('index')
    return wrapper


def derive_user_type(fun):
    """
    derive_user_type
    """
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            request.user_type = None
            return fun(request, *args, **kwargs)

        if not Account.objects.filter(user=request.user).exists():
            request.user_type = 'admin'
            return fun(request, *args, **kwargs)

        request.account = Account.objects.get(user=request.user)

        if OrdinaryUser.objects.filter(account=request.account).exists():

            request.user_type = 'ordinary'
        else:
            request.user_type = 'artist'

        return fun(request, *args, **kwargs)
    return wrapper
