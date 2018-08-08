from django.test import TestCase
from .models import Post, Comments, Like
from .forms import PostForm, CommentForm
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.urlresolvers import reverse
from loginsys.models import Profile


class PostListViewTestCase(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='user', password='top_secret')
        Post.objects.create(title='Super Important Test', text='QQ', date=timezone.now(), author=user)
        Post.objects.create(title='Test Post', text='Hello World!', date=timezone.now(), author=user)

    def test_published_posts(self):
        response = self.client.get(reverse('posts'))

        posts = response.context['posts']
        list_posts = [entry for entry in posts]

        self.assertEqual(list_posts[1].text, 'QQ')
        self.assertEqual(list_posts[0].title, 'Test Post')


class PostModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.post = Post.objects.create(title='Test Post', text='Hello World!', date=timezone.now(), author=self.user)

    def test_post_creation(self):
        self.assertEqual(self.post.author, self.user)


class CommentModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.post = Post.objects.create(title='Test Post', text='Hello World!', date=timezone.now(), author=self.user)
        self.comment = Comments.objects.create(date=timezone.now(), comment='Hi', post=self.post, author=self.user)

    def test_comment_creation(self):
        self.assertEqual(self.comment.author, self.user)
        self.assertEqual(self.comment.post, self.post)


class LikeModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.post = Post.objects.create(title='Test Post', text='Hello World!', date=timezone.now(), author=self.user)
        self.like = Like.objects.create(post=self.post, author=self.user)

    def test_like_creation(self):
        self.assertEqual(self.like.author, self.user)
        self.assertEqual(self.like.post, self.post)


class PostFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')

    def test_valid_post_data(self):
        form = PostForm({
            'title': 'Hello World!',
            'text': 'No text there.',
            'image': None,
        })
        self.assertTrue(form.is_valid())
        form.instance.author = self.user
        post = form.save()
        self.assertEqual(post.title, 'Hello World!')
        self.assertEqual(post.text, 'No text there.')


class CommentFormTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='test', password='top_secret')
        self.post = Post.objects.create(title='Test Post', text='Hello World!', date=timezone.now(), author=self.user)

    def test_valid_comment_data(self):
        form = CommentForm({
            'comment': 'Im the first!',
        })
        self.assertTrue(form.is_valid())
        form.instance.author = self.user
        form.instance.post = self.post
        comment = form.save()
        self.assertEqual(comment.comment, 'Im the first!')


class UserProfilePageTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='user', password='top_secret')
        self.profile = Profile.objects.create(user=self.user)
        self.post = Post.objects.create(title='Super Important Test', text='QQ', date=timezone.now(), author=self.user)

    def test_user_profile(self):
        response = self.client.get(reverse('user_profile', args=[self.user.username]),
                                   context={'user_profile': User.objects.get(username=self.user.username),
                                            'posts': self.post,
                                            'profile': Profile.objects.get(user_id=self.user.id)})

        # Success Redirect
        self.assertEqual(response.status_code, 200)

        # Profile Data
        profile = response.context['user_profile']
        self.assertEqual(profile.id, 1)
        self.assertEqual(profile.username, 'user')

        # Posts Data
        posts = response.context['posts']
        list_posts = [entry for entry in posts]
        self.assertEqual(list_posts[0].title, 'Super Important Test')
