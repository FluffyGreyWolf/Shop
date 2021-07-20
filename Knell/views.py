from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from Knell.forms import CreateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def registerUser(request):
    if request.user.is_authenticated:
        return redirect('/')

    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid:
            try:
                form.save()
                return redirect('/account/login')
            except:
                pass

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def loginUser(request):
    if request.user.is_authenticated:
        return redirect('/')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username or password is incorrect')
    return render(request, 'accounts/login.html')

def logoutUser(request):
    logout(request)
    return redirect('/account/login')

@login_required(login_url='/account/login/')
def profile(request):
    context = {}
    return render(request, 'accounts/profile.html', context)