from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from post.models import Post, Comments, Like
from .forms import CommentForm
from django.contrib.auth.models import User
from loginsys.forms import ProfileForm
from loginsys.models import Profile
from django.shortcuts import render, get_object_or_404

from django.views.generic.edit import CreateView
from django.views.generic.edit import DeleteView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.core.urlresolvers import reverse


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
        context = super().get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=self.kwargs['post_id'])
        context['comments'] = Comments.objects.filter(post=Post.objects.get(id=self.kwargs['post_id']).id).order_by('-id')
        context['form'] = CommentForm
        context['username'] = self.request.user.username
        context['commentator_avatars'] = Profile.objects.all()
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


class ProfilePage(TemplateView):
    template_name = 'post/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['posts'] = Post.objects.filter(author=self.request.user.id)
        return context


def avatar(request):
    user_id = request.user.id
    pk = Profile.objects.get(user_id=user_id).id
    avatar = get_object_or_404(Profile, pk=pk)

    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user_id = user_id
            form.save()
            return redirect('/me')
    else:
        form = ProfileForm()
    return render(request, 'post/add_avatar.html', {'form': form, 'username': request.user.username})


class UserProfilePage(TemplateView):
    template_name = 'post/user_profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['user_name'])
        context['user_profile'] = user
        context['posts'] = Post.objects.filter(author=user.id)
        context['avatar'] = Profile.objects.get(user_id=user.id)
        return context


class CreateOrDeleteLike(CreateView, DeleteView):
    model = Like


def like(request, post_id):
    like, created = Like.objects.get_or_create(post_id=post_id, author=request.user)
    if not created:
        like.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
