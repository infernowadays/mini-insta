from .models import Profile
from django.forms import FileInput, ModelForm


class ProfileForm(ModelForm):
    class Meta:
        model = Profile
        fields = ('photo',)
        widgets = {
            'photo': FileInput(),
        }

