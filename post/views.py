from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from post.models import Post, Comments, Like
from forms import CommentForm, PostForm
from django.contrib import auth
from django.contrib.auth.models import User
from loginsys.forms import ProfileForm
from loginsys.models import Profile
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import authenticate, login


def posts(request):
    posts = Post.objects.all().order_by('-id')
    comments = Comments.objects.all()
    html = render(request, 'post/posts.html',
                  {'posts': posts, 'comments': comments, 'username': request.user.username})
    return html


def post(request, post_id):
    comment_form = CommentForm
    args = {}
    args['post'] = Post.objects.get(id=post_id)
    args['comments'] = Comments.objects.filter(post=post_id).order_by('-id')
    args['form'] = comment_form
    args['username'] = request.user.username
    args['avatar'] = Profile.objects.all()
    return render(request, 'post/post.html', args)


def new_post(request):
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            form.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'post/new_post.html', {'form': form, 'username': request.user.username})


def like(request, post_id):
    like, created = Like.objects.get_or_create(post=Post.objects.get(id=post_id), author=request.user)
    if not created:
        like.delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def comment(request, post_id):
    if request.POST and ('pause' not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = Post.objects.get(id=post_id)
            #
            user_id = request.user.id
            comment.author = User.objects.get(id=user_id)
            #
            form.save()
            # session limit comments 30 sec
            #request.session.set_expiry(30)
            #request.session['pause'] = True
    return redirect('/post/%s' % post_id)


@login_required
def profile(request):
    args = {}
    args['username'] = request.user.username
    args['posts'] = Post.objects.filter(author=request.user.id)
    return render(request, 'post/profile.html', args)


def avatar(request):
    user_id = request.user.id
    pk = Profile.objects.get(user_id=user_id).id
    avatar = get_object_or_404(Profile, pk=pk)

    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=avatar)
        if form.is_valid():
            profile = form.save(commit=False)

            profile.user_id = user_id
            #profile.save()
            form.save()
            return redirect('/profile/me')
    else:
        form = ProfileForm()
    return render(request, 'post/add_avatar.html', {'form': form, 'username': request.user.username})


def user_profile(request, user_name):
    args = {}
    user = User.objects.get(username=user_name)
    #login(request, user)
    args['username'] = request.user.username
    args['user'] = user
    args['posts'] = Post.objects.filter(author=user.id)
    args['avatar'] = Profile.objects.get(user_id=user.id)
    return render(request, 'post/user_profile.html', args)
