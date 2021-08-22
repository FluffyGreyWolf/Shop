from django.shortcuts import redirect, render, get_object_or_404
from Knell.forms import CreateUserForm, changeEmailForm, changePictureForm, changeUsernameForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from shop.models import userProfile, orderHistory
from django.contrib.auth.models import User


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

@login_required(login_url='/account/login/')
def logoutUser(request):
    logout(request)
    return redirect('/account/login')

# View for rednering user profile page
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

# View for setting profile picture to default
@login_required(login_url='/account/login/')
def resetProfilePicture(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    user_profile, status = userProfile.objects.get_or_create(user=user)
    user_profile.profile_picture = "user_pictures/default_profile_picture.png"
    user_profile.save()
    return redirect('profile-url')

# View for changing username
@login_required(login_url='/account/login/')
def changeUsername(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    if request.method == 'POST':
        form = changeUsernameForm(request.POST, instance=user)
        newusername = form['username'].value()
        if User.objects.filter(username=newusername):
            messages.error(request, 'Username already in use!')
            return redirect('change-username')
        if form.is_valid:
            messages.success(request, 'Username changed!')
            form.save()
            return redirect('profile-url')
        else:
            return redirect('change-username')
    else:
        form = changeUsernameForm()

    context = {'form': form}
    return render(request, 'accounts/change-username.html', context)


# View for changing email
@login_required(login_url='/account/login/')
def changeEmail(request):
    user = get_object_or_404(get_user_model(), username=request.user)
    if request.method == 'POST':
        form = changeEmailForm(request.POST, instance=user)
        newemail = form['email'].value()
        if User.objects.filter(email=newemail):
            messages.error(request, 'Email already in use!')
            return redirect('change-email')
        if form.is_valid:
            messages.success(request, 'Email changed!')
            form.save()
            return redirect('profile-url')
        else:
            return redirect('change-email')
    else:
        form = changeEmailForm()

    context = {'form': form}
    return render(request, 'accounts/change-email.html', context)
    
    
    