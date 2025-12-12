# accounts/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    # followers: users who follow this user
    # related_name='following' => for a user `u`, u.following.all() هي قائمة من المستخدمين الذين u يتابعهم.
    followers = models.ManyToManyField(
        'self',
        symmetrical=False,
        related_name='following',
        blank=True,
    )

    def __str__(self):
        return self.username
