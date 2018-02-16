# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


from loginsys.models import Profile


class Post(models.Model):
    post_title = models.CharField(max_length=64)
    post_text = models.TextField(max_length=512)
    post_date = models.DateTimeField(default=timezone.now)
    post_author = models.ForeignKey(User)
    post_likes = models.IntegerField(default=0)
    post_image = models.ImageField(upload_to='post_image', blank=True)


class Comments(models.Model):
    comments_date = models.DateTimeField(default=timezone.now)
    comments_text = models.TextField(verbose_name="Tекст комментария")
    comments_post = models.ForeignKey(Post)
    comments_from = models.ForeignKey(User)


class Like(models.Model):
    like_post = models.ForeignKey(Post)
    like_author = models.ForeignKey(User)

    class Meta:
        unique_together = ("like_post", "like_author")