from django.contrib.auth import forms
from django.shortcuts import redirect, render
from django.contrib.auth.forms import UserCreationForm
from Knell.forms import CreateUserForm

def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        try:
            if form.is_valid:
                form.save()
                return redirect('login')
        except:
            return render(request, 'accounts/register.html')

    context = {'form': form}
    return render(request, 'accounts/register.html', context)

def login(request):
    return render(request, 'accounts/login.html')