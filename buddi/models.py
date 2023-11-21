from django.db import models,connection
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,primary_key=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=50,default='')
    profile_img = models.ImageField(upload_to='profile_images',default='blank-profile-pic.png')
    first_name = models.CharField(max_length=100,default='')
    last_name = models.CharField(max_length=100,default='')
    def __str__(self):
      return f'{self.user.username} (ID: {self.user.id})'




