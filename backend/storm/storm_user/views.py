from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import formats
from event.models import Event
from jsonutil import json_fail, json_success
from storm_user.forms import UserEditForm, UserAddForm, UserLoginForm


def index(request):
    events = Event.objects.all()
    json_data = {}
    for event in events:
        json_data[event.id] = {
            'id': event.id,
            'title': event.title,
            'created_by': event.created_by.username,
            'created_at': formats.date_format(event.created_at, "SHORT_DATETIME_FORMAT"),
            'description': event.description,
        }
    return json_success(request, {'events': json_data})


def login2(request):
    if request.user.is_authenticated():
        return json_fail(request, {'message': 'you already logged in!'})
    else:
        if request.POST:
            try:
                username = request.POST['username']
                password = request.POST['password']
                user = authenticate(username=username, password=password)
                if (user is not None) and user.is_active:
                    login(request, user)
                    return json_success(request, {'message': 'logged in successfully!'})
                else:
                    return json_fail(request, {'message': "Account is not correct. Try again!"})
            except KeyError:
                return json_fail(request, {'message': 'Error occurs!'})
        else:
            return json_fail(request, {'message': 'Error occurs!'})


def user_login(request):
    """
    Render and Process a form for user to login
    """
    form = UserLoginForm()

    if request.user.is_authenticated():
        #User already logged in
        return render(request, 'storm_user/user_login.html',
                      {'form': form, 'message': "You already logged in!"})

    if not (request.POST or request.GET):
        return render(request, 'storm_user/user_login.html',
                      {'form': form, 'message': "Please login..."})
    else:
        # Form POST request is submitted
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if (user is not None) and user.is_active:
                login(request, user)
                return redirect('main.main_page')
            else:
                #log in is fail
                return render(request, 'storm_user/user_login.html',
                            {'form': form, 'message': "Account is not correct. Try again!"})
        except KeyError:
            return render(request, 'storm_user/user_login.html',
                          {'form': form, 'message': "Error occurs!"})


def user_logout(request):
    logout(request)
    return redirect('main.main_page')


def user_detail(request, user_id):
    pass


def user_add(request):
    if not (request.POST or request.GET):
        form = UserAddForm()
        return render(request, 'storm_user/user_add.html', {'form': form, 'action': ''})
    else:
        #Form is submitted
        form = UserAddForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            return render(request, 'storm_user/user_add.html',
                          {'message': 'Add new user successfully!', 'form': form, 'action': ''})
        else:
            return render(request, 'storm_user/user_add.html',
                          {'message': 'Add new user fail!', 'form': form, 'action': ''})


def user_edit(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    form = UserEditForm(instance=user)
    return render(request, 'storm_user/user_edit.html',
                  {'form': form, 'action': '/storm_user/user_edit_process/' + user_id + '/'})


def user_edit_process(request):
    pass