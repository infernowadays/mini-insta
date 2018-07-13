from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    photo = models.ImageField(upload_to='profile_image', default='profile_image/default/default.jpg', blank=True)

    @classmethod
    def create(cls, user_id):
        profile = cls(user_id=user_id)
        return profile
