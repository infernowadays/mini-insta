# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from models import Profile

from django.views.generic.base import RedirectView


def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('/')
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request, 'login.html', args)
    else:
        return render(request, 'login.html', args)


class LogoutRedirectView(RedirectView):
    url = '/'
    permanent = True

    def __init__(self):
        auth.logout(self.request)
        super(LogoutRedirectView, self).__init__()


def logout(request):
    auth.logout(request)
    return redirect('/')


def register(request):
    args = {}
    args['form'] = UserCreationForm()
    if request.POST:
        newuser_form = UserCreationForm(request.POST, request.FILES)
        if newuser_form.is_valid():
            newuser_form.save()
            newuser = auth.authenticate(username=newuser_form.cleaned_data['username'],
                                        password=newuser_form.cleaned_data['password2'])
            # login new user
            auth.login(request, newuser)
            # add a default avatar to new user
            avatar = Profile.create(request.user.id)
            avatar.save()
            return redirect('/profile/me')
        else:
            args['form'] = newuser_form
    return render(request, 'register.html', args)


def profile(request):
    return render(request, 'post/profile.html', {})


