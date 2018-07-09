from django.contrib import admin
from .models import Post, Comments


class PostInline(admin.StackedInline):
    model = Comments
    extra = 2


class PostAdmin(admin.ModelAdmin):
    fields = ['title', 'text', 'date', 'image', ]
    inlines = [PostInline]
    list_filter = ['date']


admin.site.register(Post, PostAdmin)
