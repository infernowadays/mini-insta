# -*- coding: utf-8 -*-
# from __future__ import unicode_literals

from django.contrib import admin
from .models import Post, Comments


class PostInline(admin.StackedInline):
    model = Comments
    extra = 2


class PostAdmin(admin.ModelAdmin):
    fields = ['post_title', 'post_text', 'post_date', 'post_image', ]
    inlines = [PostInline]
    list_filter = ['post_date']


admin.site.register(Post, PostAdmin)
