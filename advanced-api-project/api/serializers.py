from rest_framework import serializers
from .models import Author, Book
from datetime import date


# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):
    """
        Serializes Book instances.
        - Includes all model fields.
        - Adds custom validation to ensure publication_year is not in the future.
    """
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']
        
    def validate_publication_year(self, value: int):
        """
            Field-level validation for publication_year.
            Ensures the year is <= current calendar year (no future publications).
        """
        current_year = date.today().year
        if value > current_year:
            raise serializers.ValidationError( f"publication_year cannot be in the future (got {value}, current year is {current_year}).")
        return value
            
        
        
# Serializer for Author model
class AuthorSerializer(serializers.ModelSerializer):
    """
        Serializes Author instances.
        - name: The author's name.
        - books: Nested list of the author's related books (read-only), using BookSerializer.
        Because Book.author uses related_name='books', we can expose `books` directly.
        This is a *read-only nested representation*; create/update is handled via separate Book writes.
        If you need writable nested creates, you'd override create()/update().
    """
    books = BookSerializer(many=True, read_only=True)
    
    class Meta:
        model = Author
        fields = ['id', 'name', 'books']        