from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from main.templatetags.user_permission_tags import can_retrieve_user, can_create_user, can_list_user, can_update_user
from storm_user.forms import UserLoginForm, UserCreateForm, UserUpdateForm
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
                      {'form': form, 'message': ""})
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
    #Check permission
    try:
        userprofile = UserProfile.objects.get(user=User.objects.get(pk=user_id))
    except(KeyError, UserProfile.DoesNotExist):
        return HttpResponse("Dont exist this user!")

    if not can_retrieve_user(request.user, userprofile):
        return render(request, "main/no_permission.html")
    else:
        return render(request, 'storm_user/user_retrieve.html', {"userprofile": userprofile})


def user_create(request):
    #Check permission
    if not can_create_user(request.user):
        return render(request, "main/no_permission.html")

    if not (request.POST or request.GET):
        form = UserCreateForm()
        return render(request, 'storm_user/user_create.html', {'form': form})
    else:
        #Form is submitted
        form = UserCreateForm(request.POST)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            form.save_m2m()
            userprofile = UserProfile(name=form.cleaned_data.get('name'),
                                      phone_number=form.cleaned_data.get('phone_number'),
                                      user=model_instance)
            userprofile.save()
            return redirect('user.user_list')
        else:
            return render(request, 'storm_user/user_create.html', {'form': form})


def user_update(request, user_id):

    #Check permission
    user = get_object_or_404(User, pk=user_id)
    userprofile = UserProfile.objects.get(user=user)
    if not can_update_user(request.user, userprofile):
        return render(request, "main/no_permission.html")

    if not (request.POST or request.GET):
        user = get_object_or_404(User, pk=user_id)
        print user.groups.all()
        form = UserUpdateForm(instance=user)
        return render(request, 'storm_user/user_update.html', {'form': form})
    else:
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            model_instance = form.save(commit=False)
            model_instance.save()
            form.save_m2m()
            userprofile = UserProfile.objects.get(user=model_instance)
            userprofile.name = form.cleaned_data.get('name')
            userprofile.phone_number = form.cleaned_data.get('phone_number')
            userprofile.save()
            return HttpResponseRedirect(reverse('user.user_retrieve', args=(user_id,)))
        else:
            return render(request, 'storm_user/user_update.html/',
                          {'message': 'update user fail!', 'form': form})


def user_list(request):

    #Check permission
    if not can_list_user(request.user):
        return render(request, "main/no_permission.html")

    user_list = UserProfile.objects.all().order_by("-id")
    return render(request, "storm_user/user_list.html", {'user_list': user_list})
