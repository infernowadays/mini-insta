from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from post.models import Post, Comments, Like
from forms import CommentForm, PostForm
from django.contrib.auth.models import User
from loginsys.forms import ProfileForm
from loginsys.models import Profile
from django.shortcuts import render, get_object_or_404

from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView


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
        context = super(PostDetailView, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(id=Post.objects.get(id=self.kwargs['post_id']).id)
        context['comments'] = Comments.objects.filter(post=Post.objects.get(id=self.kwargs['post_id']).id).order_by('-id')
        context['form'] = CommentForm
        context['username'] = self.request.user.username
        context['avatar'] = Profile.objects.all()
        return context


class NewPostView(CreateView):
    template_name = 'post/new_post.html'
    model = Post
    fields = ['title', 'text', 'image']
    success_url = '/'
    # fields = '__all__'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super(NewPostView, self).form_valid(form)


class CommentView(CreateView):
    template_name = 'post/comment.html'
    model = Comments
    fields = ['comment']

    def form_valid(self, form):
        form.instance.post = Post.objects.get(id=self.kwargs['post_id'])
        form.instance.author = User.objects.get(id=self.request.user.id)
        return super(CommentView, self).form_valid(form)

    def get_success_url(self):
        return '/post/' + str(Post.objects.get(id=self.kwargs['post_id']).id)


class ProfilePage(TemplateView):
    template_name = 'post/profile.html'

    def get_context_data(self, **kwargs):
        context = super(ProfilePage, self).get_context_data(**kwargs)
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
            return redirect('/profile/me')
    else:
        form = ProfileForm()
    return render(request, 'post/add_avatar.html', {'form': form, 'username': request.user.username})


class UserProfilePage(TemplateView):
    template_name = 'post/profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserProfilePage, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.kwargs['user_name'])
        context['user'] = user
        context['posts'] = Post.objects.filter(author=user.id)
        context['avatar'] = Profile.objects.get(user_id=user.id)
        return context


def like(request, post_id):
    like, created = Like.objects.get_or_create(post_id=post_id, author=request.user)
    if not created:
        like.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))