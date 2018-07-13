from django.shortcuts import render, redirect
from django.contrib import auth
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

from django.views.generic.base import RedirectView
from django.views.generic.edit import FormView
from django.http import HttpResponse


class LoginRedirectView(FormView):
    template_name = 'login.html'
    form_class = UserCreationForm
    success_url = '/me'

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(self.request, user)
        else:
            return HttpResponse('Login or pw incorrect')
        return super().form_valid(form)


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

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            auth.logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


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


