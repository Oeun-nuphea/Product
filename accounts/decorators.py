from django.http import HttpResponse
from django.shortcuts import redirect


def unauthenticated_user(view_func):   #loginPage in views.py become a paramenter of this view_func
    def wrapper_func(request, *args, **kwargs):
        if request.user.is_authenticated:
            return  redirect('home')    
        else:
            

        # **kwargs(keyword arguments) it catches all of keywords of arguments
        # *args it cathces all of arguments
        # even no of them use it still work correctly 
            return view_func(request, *args, **kwargs)
    return wrapper_func


def allowed_user(allow_roles=[]):
    def decorator(view_func):
        def wrapper_func(request, *args, **kwargs):

            group = None

            if request.user.groups.exists():
                group = request.user.groups.all()[0].name

            if group in allow_roles:
                return view_func(request, *args, **kwargs)
            
            else: 
                return HttpResponse('You are not allowed to view this page')
        return wrapper_func
    return decorator


def admin_only(view_func):
    def wrapper_func(request, *args, **kwargs):
        group = None
        
        if request.user.groups.exists():

            group = request.user.groups.all()[0].name

        if group == 'customer':

            return redirect('user_page')
        
        if group == 'admin':
            return view_func(request, *args, **kwargs)
    return wrapper_func