from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm
from .models import Record


def home(request: 'HttpRequest'):
    records = Record.objects.all() if request.user.is_authenticated else None
    return render(request, 'home.html', {'records': records})


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


def register_user(request: 'HttpRequest'):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if not form.is_valid():
            return render(request, 'register.html', {'form': form})

        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(
            request, 'You have successfully registered! Welcome!')
        return redirect('home')

    form = SignUpForm()
    return render(request, 'register.html', {'form': form})
