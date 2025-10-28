from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile
from .models import Post
from .models import Comment
from taggit.forms import TagWidget

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio', 'profile_picture']  


class PostForm(forms.ModelForm):
    tags = forms.CharField(widget=TagWidget(attrs={'class': 'form-control'}))  # <- direct assignment

    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }
        

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
        labels = {
            'content': 'Your Comment',
        }        
              
dummy = TagWidget()              