# -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
                  {'posts': posts, 'comments': comments, 'username': auth.get_user(request).username})
    return html


def post(request, post_id):
    comment_form = CommentForm
    args = {}
    args['post'] = Post.objects.get(id=post_id)
    args['comments'] = Comments.objects.filter(comments_post_id=post_id).order_by('-id')
    args['form'] = comment_form
    args['username'] = auth.get_user(request).username
    args['avatar'] = Profile.objects.all()
    return render(request, 'post/post.html', args)


def new_post(request):
    if request.POST:
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            user_id = auth.get_user(request).id
            post.post_author = User.objects.get(id=user_id)
            form.save()
            return redirect('/')
    else:
        form = PostForm()
    return render(request, 'post/new_post.html', {'form': form, 'username': auth.get_user(request).username})


def like(request, post_id):
    user = auth.get_user(request).username
    if not user:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    user_id = User.objects.get(id=auth.get_user(request).id)
    post = Post.objects.get(id=post_id)
    if Like.objects.filter(like_post=post_id, like_author=user_id).exists():
        Like.objects.get(like_post=Post.objects.get(id=post_id), like_author=user_id).delete()
        post.post_likes -= 1
        post.save()
    else:
        like = Like(like_post=Post.objects.get(id=post_id), like_author=user_id)
        like.save()

        post.post_likes += 1
        post.save()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def comment(request, post_id):
    if request.POST and ("pause" not in request.session):
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.comments_post = Post.objects.get(id=post_id)
            #
            user_id = auth.get_user(request).id
            comment.comments_from = User.objects.get(id=user_id)
            #
            form.save()
            # session limit comments 30 sec
            #request.session.set_expiry(30)
            #request.session['pause'] = True
    return redirect('/post/%s' % post_id)


@login_required
def profile(request):
    args = {}
    args['username'] = auth.get_user(request).username
    args['posts'] = Post.objects.filter(post_author=auth.get_user(request).id)
    return render(request, 'post/profile.html', args)


def avatar(request):
    user_id = auth.get_user(request).id
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
    return render(request, 'post/add_avatar.html', {'form': form, 'username': auth.get_user(request).username})


def user_profile(request, user_name):
    args = {}
    user = User.objects.get(username=user_name)
    #login(request, user)
    args['username'] = auth.get_user(request).username
    args['user'] = user
    args['posts'] = Post.objects.filter(post_author=user.id)
    args['avatar'] = Profile.objects.get(user_id=user.id)
    return render(request, 'post/user_profile.html', args)