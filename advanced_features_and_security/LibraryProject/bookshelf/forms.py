from django import forms
from .models import Book

class ExampleForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date']
        
    # Custom validation example
    def clean_title(self):
        title = self.cleaned_data['title']
        if len(title) < 3:
            raise forms.ValidationError("Title must be at least 3 characters long.")
        return title
