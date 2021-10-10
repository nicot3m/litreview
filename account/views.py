from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from .forms import CreateUser, LoginUser, SubscriptionForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UserFollows
from django.db import IntegrityError
from django.contrib.auth.models import User


# Create your views here.
def signup(request):
    """signup a new user"""
    form = CreateUser()
    if request.method == 'POST':
        form = CreateUser(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=password)
            login(request, user)
            messages.success(request, 'Compte créé avec succès pour ' + username)
            return redirect('feed')
    context = {'form': form}
    return render(request, 'account/signup.html', context)


def user_login(request):
    """login a user"""
    if request.method == 'POST':
        form = LoginUser(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('feed')
        else:
            messages.info(request, "utilisateur ou mot de passe non reconnu")
    else:
        form = LoginUser()
    context = {'form': form}
    return render(request, 'account/login.html', context)


def user_logout(request):
    """logout a user"""
    logout(request)
    return redirect('login')


@login_required(login_url='account/login')
def subscribe(request):
    """follow a new user"""
    subscriber_list = UserFollows.objects.filter(followed_user=request.user)
    followed_user_list = UserFollows.objects.filter(user=request.user)
    all_users = User.objects.all()
    if request.method == "GET":
        form = SubscriptionForm()
        return render(request, 'account/subscribe.html', locals())

    elif request.method == 'POST':
        form = SubscriptionForm(request.POST)
        if form.is_valid():
            #followed_user = form.cleaned_data['followed_user']
            modif_form = form.save(commit=False)
            username = form.cleaned_data['username']
            user = request.user
            try:
                followed_user = User.objects.get(username=modif_form.username)
            except Exception:
                message = "utilisateur non reconnu"
                return render(request, 'account/subscribe.html', locals())

            if followed_user == user:
                message = "Vous ne pouvez vous suivre!"
            else:
                try:
                    user_follow = UserFollows.objects.create(user=user, followed_user=followed_user)
                    user_follow.save()
                    message = "Utilisateur ajouté"
                except IntegrityError:
                    message = "Utilisateur déjà suivi!"

            return render(request, 'account/subscribe.html', locals())


@login_required(login_url='account/login')
def unsubscribe(request, id_user_follow):
    """Remove a followed user"""
    user_follow = get_object_or_404(UserFollows, pk=id_user_follow)
    user_follow.delete()
    return redirect('subscribe')
