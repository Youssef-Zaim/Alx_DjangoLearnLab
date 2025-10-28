from rest_framework import serializers
from .models import Book

# Book serializer
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'  # Include all fields from the Book model