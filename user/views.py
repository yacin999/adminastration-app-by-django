from django.shortcuts import render, redirect
from .forms  import RegisterForm, UserForm, StaffForm
from .models import Staff, StaffPermission
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):

    
    print("is this user staff !!! ", request.user.is_staff)

    if (request.method == 'POST'):
        userform = RegisterForm(request.POST)

        if userform.is_valid():
            user = userform.save(commit=False)
            user.set_password(userform.cleaned_data["password1"])
            user.save()
            staff = Staff.objects.create(user=user)
    else:
        userform = RegisterForm()

    context = {
        'title': 'new user',
        'user': userform,
    }
    
    return render(request, "user/register.html", context)

def login_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser or user.staff.accepted:
                login(request, user)
                return redirect('admin_panel')
            else:
                messages.error(request, 'wait for the Admin until he confirm your accout')
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
