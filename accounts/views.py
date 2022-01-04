from django.shortcuts import render
from .forms import Login
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from resort.models import Activity


def user_login(request):
    if request.method=="POST":
        form=Login(request.POST)
        if form.is_valid():
            data=form.cleaned_data
            user= authenticate(request,username=data['username'],password=data['password'])
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
        form= UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.add_message(request,messages.SUCCESS,"User has been added")
            return redirect('/login')
        else:
            messages.add_message(request,messages.ERROR,"Invalid input, Try again")
            return render(request,'accounts/register.html',{'register_form':form})
    context={
        'register_form':UserCreationForm,
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