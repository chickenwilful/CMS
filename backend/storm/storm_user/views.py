from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from storm_user.forms import UserLoginForm, UserCreateForm, UserProfileCreateForm
from storm_user.models import UserProfile


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


def user_retrieve(request, user_id):
    try:
        userprofile = UserProfile.objects.filter(user=user_id)
    except (KeyError, UserProfile.DoesNotExist):
        return HttpResponse("404 NOT FOUND")
    else:
        return render(request, 'storm_user/user_retrieve.html', {"userprofile": userprofile})


def user_create(request):
    if not (request.POST or request.GET):
        form = UserCreateForm()
        return render(request, 'storm_user/user_create.html', {'form': form, 'action': ''})
    else:
        #Form is submitted
        form = UserCreateForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            userprofile = UserProfile(user = model_instance)

            form.save()
            userprofileform.save()
            return render(request, 'storm_user/user_create.html',
                          {'message': 'Add new user successfully!', 'form': form, 'action': ''})
        else:
            return render(request, 'storm_user/user_create.html',
                          {'message': 'Add new user fail!', 'form': form, 'action': ''})


def user_update():
    #TODO: user_update implement
    pass
