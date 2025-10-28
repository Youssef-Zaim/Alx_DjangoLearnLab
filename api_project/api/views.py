from rest_framework import generics
from .models import Book
from rest_framework import viewsets
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser  

# Class-based view to handle book listing
class BookList(generics.ListAPIView):
    queryset = Book.objects.all()  # Fetch all book records
    serializer_class = BookSerializer  # Use the BookSerializer for serialization
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access this view

# BookViewSet class handles all CRUD operations for the Book model
# Users must be authenticated to access these endpoints.
# Admin users can create books, while regular authenticated users can view and edit them.
# Book set view
class BookViewSet(viewsets.ModelViewSet):
    """"
      Book set view that handles all the CRUD operations for books.
      
    """
    queryset = Book.objects.all() # Fetch all book records
    serializer_class = BookSerializer  # Use the BookSerializer for serialization
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated to access this view
    
    
    # Function for only admin users to create books
    def get_permissions(self):
        if self.action == 'create':
             return [IsAdminUser()] # Only allow admin users to create books
        return super().get_permissions() # Return default permissions for other actions