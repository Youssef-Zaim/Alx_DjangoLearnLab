from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from taggit.managers import TaggableManager

# Post model
class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    
    tags = TaggableManager()
    
    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post-detail', kwargs={'pk': self.pk})
    
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile')
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True) 
    
    def __str__(self):
        return f"{self.user.username}'s profile"
    
    
class Comment(models.Model):
    post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.post.title}"

    def get_absolute_url(self):
        # Redirect back to the post detail page after comment CRUD
        return reverse('post-detail', kwargs={'pk': self.post.pk})       
