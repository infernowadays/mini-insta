# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from forms import ProfileForm
from models import Profile

from django.http.response import HttpResponse
from django.http import HttpResponseRedirect


# Create your views here.

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
            #login new user
            auth.login(request, newuser)
            #add a default avatar to new user
            avatar = Profile.create(auth.get_user(request).id)
            avatar.save()
            return redirect('/profile')
        else:
            args['form'] = newuser_form
    return render(request, 'register.html', args)


def profile(request):
	return render(request, 'post/profile.html', {})

