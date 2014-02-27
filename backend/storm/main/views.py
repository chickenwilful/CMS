from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def main_page(request):
    message = request.session.get('login_message', '')
    if 'login_message' in request.session:
        del request.session['login_message']
    return render(request, "main/main_page.html", {'login_message': message})


def user_login_process(request):
    if not request.user.is_authenticated():
        try:
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)
            if (user is not None) and user.is_active:
                login(request, user)
                request.session['login_message'] = 'Login successful'
                return redirect('main.main_page')
        except (KeyError, User.DoesNotExist):
            request.session['login_message'] = 'Cannot login'

        request.session['login_message'] = 'Cannot login'
        return redirect('main.user_login')
    else:
        request.session['login_message'] = 'You are already logged in'
        return redirect('main.main_page')


def user_login(request):
    login_message = request.session.get('login_message', 'Please login')
    if 'login_message' in request.session:
        request.session['login_message']
    return render(request, 'main/user_login.html', {'login_message': login_message})


def user_logout(request):
    logout(request)
    request.session['login_message'] = 'Goodbye'
    return redirect('main.main_page')



