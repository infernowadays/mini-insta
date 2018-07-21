from django.shortcuts import redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile
from django.utils.http import is_safe_url
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login, logout, authenticate
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.views.generic import FormView, RedirectView, CreateView


class LoginView(FormView):
    success_url = '/profile/me'
    form_class = AuthenticationForm
    template_name = 'login.html'
    redirect_field_name = REDIRECT_FIELD_NAME

    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())

        # If the test cookie worked, go ahead and
        # delete it since its no longer needed
        if self.request.session.test_cookie_worked():
            self.request.session.delete_test_cookie()

        return super().form_valid(form)

    def get_success_url(self):
        redirect_to = self.request.GET.get(self.redirect_field_name)
        if not is_safe_url(url=redirect_to, host=self.request.get_host()):
            redirect_to = self.success_url
        return redirect_to


class LogoutView(RedirectView):
    url = '/'

    def get_redirect_url(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            logout(self.request)
        return super().get_redirect_url(*args, **kwargs)


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = '/profile/me'
    template_name = 'register.html'

    def form_valid(self, form):
        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password2')

        user = UserCreationForm(self.request.POST, self.request.FILES)
        user.save()

        user = authenticate(username=username, password=password)
        login(self.request, user)

        # add a default avatar to new user
        avatar = Profile.create(self.request.user.id)
        avatar.save()
        return redirect('/profile/me')

