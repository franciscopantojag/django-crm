from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request: 'HttpRequest'):
    return render(request, 'home.html', {})


def login_user(request: 'HttpRequest'):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)

    if user is None:
        messages.success(
            request, 'There was an Error logging in, please try again')
        return redirect('home')

    login(request, user)
    messages.success(request, 'You have been logged in')
    return redirect('home')


def logout_user(request: 'HttpRequest'):
    logout(request)
    messages.success(request, 'You have been logged out')
    return redirect('home')
