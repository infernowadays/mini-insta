from django import forms
from models import Comments, Post


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comments
        widgets = {
            'comments_text': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }
        fields = ('comments_text',)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('post_title', 'post_text', 'post_image', )
