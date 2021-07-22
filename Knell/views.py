from django.shortcuts import redirect, render, get_object_or_404
from Knell.forms import CreateUserForm, changePictureForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from shop.models import userProfile, orderHistory


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
    user = get_object_or_404(get_user_model(), username=request.user)
    user_profile, status = userProfile.objects.get_or_create(user=user)
    orders = orderHistory.objects.filter(owner=user)
    if request.method == 'POST':
        form = changePictureForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            
            return redirect('profile-url')
    else:
        form = changePictureForm()
    context = {'user_profile': user_profile, 'orders': orders, 'form': form}
    return render(request, 'accounts/profile.html', context)

@login_required(login_url='/account/login/')
def resetProfilePicture(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    user_profile, status = userProfile.objects.get_or_create(user=user)
    user_profile.profile_picture = "user_pictures/default_profile_picture.png"
    user_profile.save()
    return redirect('profile-url')