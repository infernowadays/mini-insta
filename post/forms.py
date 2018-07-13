from django import forms
from .models import Comments, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }
        fields = ('comment',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
