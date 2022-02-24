from django.shortcuts import redirect

def unauthenticated_user(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('/groceries/home')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function

def admin_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return view_function(request, *args, **kwargs)
        else:
            return redirect('/groceries/home')
    return wrapper_function

def user_only(view_function):
    def wrapper_function(request, *args, **kwargs):
        if request.user.is_staff:
            return redirect('/admins/admin_dashboard')
        else:
            return view_function(request, *args, **kwargs)
    return wrapper_function