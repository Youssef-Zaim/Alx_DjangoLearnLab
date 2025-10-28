from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager 

# User model extended from AbstractUser
class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    following = models.ManyToManyField('self', blank=True, related_name='followed_by', symmetrical=False)
    
    def __str__(self):
        return self.username
