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

    def test_user_is_not_authenticated(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)


class SignUpViewTestCase(TestCase):
    def setUp(self):
        self.user1 = User.objects.create_user(username='test1', password='top_secret1')
        self.user2 = User.objects.create_user(username='test2', password='top_secret2')

    def test_users_created(self):
        self.assertEqual(User.objects.count(), 2)


class ProfileModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.profile = Profile.create(self.user.id)

    def test_profile_creation(self):
        self.assertEqual(self.profile.user, self.user)
