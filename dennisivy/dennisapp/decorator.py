from django.http import HttpResponse
from django.shortcuts import redirect

def unauthenticated_user(view_func):
    def wrapped_func(req, *args, **kwargs):
        if req.user.is_authenticated:
            return redirect('dashboard')
        else:
            return view_func(req, *args, **kwargs)
    return wrapped_func

def allowed_users(allowed_roles = []):
    def decorators(view_func):
        def wrapper(req, *args, **kwargs):
            group = None
            if req.user.groups.exists():
                group = req.user.groups.all()[0].name
            if group in allowed_roles:
                print('Working', allowed_roles)
                return view_func(req, *args, **kwargs)
            else:
                return HttpResponse('Your not authorised to this page')
        return wrapper
    return decorators

def admin_only(view_func):
    def wrapper(req, *args, **kwargs):
        group = None
        if req.user.groups.exists():
            group = req.user.groups.all()[0].name
        if group == 'admin':
            return view_func(req, *args, **kwargs)
        if group == 'customer':
            return redirect('users')

    return wrapper





