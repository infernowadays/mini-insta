from django.http import HttpResponseRedirect
from post.models import Post, Comments, Like
from .forms import CommentForm
from django.contrib.auth.models import User
from loginsys.models import Profile
from django.views.generic import CreateView, ListView, TemplateView, UpdateView, View
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


class PostListView(ListView):
    template_name = 'post/posts.html'
    model = Post
    context_object_name = 'posts'
    queryset = Post.objects.order_by('-id')
    paginate_by = 5


class PostDetailView(ListView):
    template_name = 'post/post.html'
    model = Comments

    def get_context_data(self, **kwargs):
        post = Post.objects.get(id=self.kwargs['post_id'])
        context = super().get_context_data(**kwargs)
        context['post'] = post
        context['comments'] = post.comments.all().order_by('-id')
        context['form'] = CommentForm
        context['username'] = self.request.user.username
        context['commentator_profiles'] = Profile.objects.all()
        return context


class NewPostView(CreateView):
    template_name = 'post/new_post.html'
    model = Post
    fields = ['title', 'text', 'image']
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class CommentView(CreateView):
    template_name = 'post/comment.html'
    model = Comments
    fields = ['comment']

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])
        form.instance.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('post', args=[self.kwargs['post_id']])


@method_decorator(login_required, name='dispatch')
class ProfilePage(TemplateView):
    template_name = 'post/profile.html'

    def get_context_data(self, **kwargs):
        if not self.request.user.is_anonymous():
            user = User.objects.get(id=self.request.user.id)
            context = super().get_context_data(**kwargs)
            context['posts'] = user.posts.all()
            return context
        return None


class UserProfilePage(TemplateView):
    template_name = 'post/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['user_name'])
        context['user_profile'] = user
        context['posts'] = user.posts.all()
        context['profile'] = Profile.objects.get(user_id=user.id)
        return context


class LikeView(View):
    model = Like

    def get(self, request, post_id):
        like, created = Like.objects.get_or_create(post_id=post_id, author_id=request.user.id)
        if not created:
            like.delete()

        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class ChangeAvatarView(UpdateView):
    model = Profile
    fields = ['photo']
    template_name = 'post/add_avatar.html'

    def get_object(self, queryset=None):
        pk = self.request.user.profile
        return pk

    def get_success_url(self):
        return reverse('profile')
