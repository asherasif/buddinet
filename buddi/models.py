from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField(default=0)
    email = models.EmailField()
    password = models.CharField(max_length=50)
    profile_img = models.ImageField(upload_to='profile_images',default='blank-profile-pic.png')
    first_name = models.CharField(max_length=100,default=None)
    last_name = models.CharField(max_length=100,default=None)

def __str__(self):
    return self.user.username

    
    