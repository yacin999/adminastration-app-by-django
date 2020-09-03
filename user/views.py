from django.shortcuts import render, redirect
from .forms  import RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


# Create your views here.


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            #messages.success(request, 'you have successfuly registred')
            return redirect('/')
    else:
        form = RegisterForm()

    return render(request, 'user/register.html', {
        'form': form
    })


def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('all_teachers')
        else:
            messages.warning(request, 'there is an error in the username or the password ')
        

    return render(request, 'user/login.html', {
        'title': 'login',
    })

def logout_user(request):
    logout(request)
    template_name = 'user/logout.html'
    context = {'title': 'logout'}

    return render(request, template_name, context)
