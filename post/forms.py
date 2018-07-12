from django import forms
from models import Comments, Post


class CommentForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True

    class Meta:
        model = Comments
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 2, 'cols': 30}),
        }
        fields = ('comment',)


class PostForm(forms.ModelForm):
    def init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['comment'].required = True

    class Meta:
        model = Post
        fields = ('title', 'text', 'image')
