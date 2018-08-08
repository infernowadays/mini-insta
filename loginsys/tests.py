from django.test import TestCase
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from .models import Profile


class LoginViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')

    def test_user_is_authenticated(self):
        logged_in = self.client.login(username=self.user.username, password='top_secret')
        self.assertTrue(logged_in)


class LogoutViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.client.login(username=self.user.username, password='top_secret')

    def test_user_is_not_authenticated_after_logout(self):
        self.client.get(reverse('logout'))
        self.assertEqual(self.client.session.get('_auth_user_id'), None)

    def test_not_authenticated_user_redirect(self):
        self.client.get(reverse('logout'))
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)


class SignUpViewTestCase(TestCase):
    def test_users_created(self):
        response = self.client.post(reverse('register'),
                                    data={'username': 'alice',
                                          'password1': 'alice@example.com',
                                          'password2': 'alice@example.com'})
        # Redirect to Profile Page
        self.assertEqual(response.status_code, 302)

        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)

        # Get context data from Profile Page
        profile = response.context['user']
        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.username, 'alice')


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.profile = Profile.create(self.user.id)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
