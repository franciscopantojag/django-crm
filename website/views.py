from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponseNotAllowed
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .forms import SignUpForm, AddRecordForm
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
    form = SignUpForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        username = form.cleaned_data['username']
        password = form.cleaned_data['password1']
        user = authenticate(request, username=username, password=password)
        login(request, user)
        messages.success(request, 'You have successfully registered! Welcome!')
        return redirect('home')

    return render(request, 'register.html', {'form': form})


def record(request: 'HttpRequest', record_id: 'int'):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in to access this page')
        return render(request, 'record.html')

    customer_record = get_object_or_404(Record, id=record_id)
    return render(request, 'record.html', {'customer_record': customer_record})


def add_record(request: 'HttpRequest'):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in ...')
        return redirect(request, 'home')

    form = AddRecordForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'You have successfully created a record!')
        return redirect('home')

    return render(request, 'add_record.html', {'form': form})


def update_record(request: 'HttpRequest', record_id: 'int'):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in ...')
        return redirect('home')

    current_record = get_object_or_404(Record, id=record_id)
    form = AddRecordForm(request.POST or None, instance=current_record)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'You have successfully updated a record!')
        return redirect('home')

    return render(request, 'add_record.html', {'form': form})


def delete_record(request: 'HttpRequest', record_id: 'int'):
    if not request.user.is_authenticated:
        messages.success(request, 'You must be logged in ...')
        return redirect('home')

    get_object_or_404(Record, id=record_id).delete()
    messages.success(request, "Record Deleted Successfully...")
    return redirect('home')
