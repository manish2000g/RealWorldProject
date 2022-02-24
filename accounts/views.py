from django.shortcuts import render
from .forms import Login
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import ProfileForm,CreateUserForm
from accounts.auth import user_only, admin_only
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from resort.models import Activity
from .models import Profile


def user_login(request):
    if request.method == "POST":
        form = Login(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request, username=data['username'], password=data['password'])
            print(user)
            if user is not None:
              if user.is_staff:
                login(request,user)
                return redirect('/admins/admin_dashboard')
              elif not user.is_staff:
                login(request,user)
                return redirect('/resort/home')

            else:
                messages.add_message(request,messages.ERROR,"Can't find the user")
                return render(request,'accounts/login.html',{'login_form':form})
    context={
        'login_form':Login,
        'activate_login':'active'
    }
    return render(request,'accounts/login.html',context)

def user_register(request):
    if request.method=='POST':
        form= CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.save()
            Profile.objects.create(user=user, username=user.username,
                                   email=user.email)
            messages.add_message(request, messages.SUCCESS, "User has been added")
            return redirect('/login')
        else:
            messages.add_message(request,messages.ERROR,"Invalid input, Try again")
            return render(request,'accounts/register.html',{'register_form':form})
    context={
        'register_form':CreateUserForm(),
        'activate_register':'active'
    }
    return render(request,'accounts/register.html',context)


def homepage(request):
    activities = Activity.objects.all().order_by('-id')[:3]
    context = {
        'activities': activities
    }
    return redirect('/resort/home')


def user_logout(request):
    logout(request)
    return redirect('/login')


@login_required
@admin_only
def get_users(request):
    users = User.objects.filter(is_staff=0).order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'accounts/users.html', context)


@login_required
@admin_only
def get_users(request):
    users = User.objects.filter(is_staff=0).order_by('-id')
    context = {
        'users': users
    }
    return render(request, 'accounts/users.html', context)


@login_required
@admin_only
def get_admins(request):
    admins = User.objects.filter(is_staff=1).order_by('-id')
    context = {
        'admins': admins
    }
    return render(request, 'accounts/admins.html', context)


@login_required
@admin_only
def deactivate_admin(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Admin Disabled')
    return redirect('/admins/admins')


@login_required
@admin_only
def deactivate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = False
    user.save()
    messages.add_message(request, messages.SUCCESS, 'User Disabled')
    return redirect('/admins/users')


#
@login_required
@admin_only
def activate_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'User Enabled')
    return redirect('/admins/users')


@login_required
@admin_only
def activate_admin(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_active = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Admin Enabled')
    return redirect('/admins/admins')


@login_required
@admin_only
def promote_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_staff = True
    user.save()
    messages.add_message(request, messages.SUCCESS, 'User promoted to admin')
    return redirect('/admins/admins')


@login_required
@admin_only
def demote_user(request, user_id):
    user = User.objects.get(id=user_id)
    user.is_staff = False
    user.save()
    messages.add_message(request, messages.SUCCESS, 'Admin demoted to user')
    return redirect('/admins/users')


@login_required
@user_only
def profile(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated Successfully')
            return redirect('/profile')
    context = {
        'form': ProfileForm(instance=profile),
        'activate_profile': 'active'
    }
    return render(request, 'accounts/profile.html', context)


@login_required
@admin_only
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.add_message(request, messages.SUCCESS, 'Password Changed Successfully')
            if request.user.is_staff:
                return redirect('/admins')
            else:
                return redirect('/resort/home')
        else:
            messages.add_message(request, messages.ERROR, 'Please verify the form fields')
            return render(request, 'accounts/pwchange.html', {'password_change_form': form})
    context = {
        'password_change_form': PasswordChangeForm(request.user)
    }
    return render(request, 'accounts/pwchange.html', context)
