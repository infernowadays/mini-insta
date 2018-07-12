# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Post(models.Model):
    title = models.CharField(max_length=64, blank=False)
    text = models.TextField(max_length=512, blank=False)
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User)
    image = models.ImageField(upload_to='post_image', blank=True)


class Comments(models.Model):
    date = models.DateTimeField(default=timezone.now)
    comment = models.TextField(verbose_name='Tекст комментария', blank=False)
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)


class Like(models.Model):
    post = models.ForeignKey(Post)
    author = models.ForeignKey(User)

    class Meta:
        unique_together = ('post', 'author')
