from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import render, redirect


def main_page(request):
    message = request.session.get('login_message', '')
    if 'login_message' in request.session:
        del request.session['login_message']
    return render(request, "main/main_page.html", {'login_message': message})


