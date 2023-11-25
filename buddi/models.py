from django.db import models,connection
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime
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


class Post(models.Model):
   id = models.UUIDField(primary_key=True,default=uuid.uuid4)
   user = models.CharField(max_length=100)
   image = models.ImageField(upload_to='post images')
   text = models.TextField()
   created_at = models.DateTimeField(default=datetime.now)
   no_of_likes = models.IntegerField(default=0)

   def __str__(self):
      return self.user
   

class LikePost(models.Model):
   post_id = models.CharField(max_length=100)   
   username = models.CharField(max_length=100)

   def __str__(self):
      return self.username


