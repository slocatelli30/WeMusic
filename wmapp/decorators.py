from django.shortcuts import redirect
from .models import OrdinaryUser, Account


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
