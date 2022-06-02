from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from .forms import UserForm


@login_required
def user_logout(request):
    logout(request)
    return redirect('login')


def register(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/')
        return render(request, 'clicker/register.html', {'form': form})
    form = UserForm()
    return render(request, 'clicker/register.html', {'form': form})


def user_login(request):
    form = UserForm()

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return redirect('/')

        return render(request, 'clicker/login.html', {'form': form, 'invalid': True})

    return render(request, 'clicker/login.html', {'form': form})


# todo
@login_required
def play(request):
    return {"Hello"}
