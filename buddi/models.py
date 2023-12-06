from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
import uuid  
from datetime import datetime

User = get_user_model()

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    email = models.EmailField(default='')
    password = models.CharField(max_length=50, default='')
    profile_img = models.ImageField(upload_to='profile_images', default='blank-profile-pic.png')
    first_name = models.CharField(max_length=100, default='')
    last_name = models.CharField(max_length=100, default='')

    def __str__(self):
        return f'{self.user.username} (ID: {self.user.id})'

class comments(models.Model):
    comment_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey('Post', on_delete=models.CASCADE, default=1)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default=1) 
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='post images')
    text = models.TextField()
    created_at = models.DateTimeField(default=datetime.now)
    no_of_likes = models.IntegerField(default=0)
    comments1 = models.ManyToManyField(comments, related_name='comments')

    def __str__(self):
        return f'Post by {self.user.username}'

class LikePost(models.Model):
    post_id = models.CharField(max_length=100)   
    username = models.CharField(max_length=100)

    def __str__(self):
        return self.username

class Followers(models.Model):
    
    connection_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE, default=777)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE, default=777)

    def __str__(self):
        return f'{self.follower.username} follows {self.followed.username}'
