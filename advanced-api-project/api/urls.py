from django.urls import path
from .views import (
    BookListView, BookDetailView, BookCreateView, BookUpdateView, BookDeleteView
)

urlpatterns = [
    # Read
    path("books/", BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="book-detail"),
    
    # Create
    path("books/create/", BookCreateView.as_view(), name="book-create"),
    
    # Update - both patterns (order-insensitive matchers)
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="book-update"),
    path("books/update/<int:pk>/", BookUpdateView.as_view(), name="bokk-update-alt"),
    
    # Delete
    path("books/<int:pk>/delete/", BookDeleteView.as_view(), name="book-delete"),
    path("books/delete/<int:pk>/", BookDeleteView.as_view(), name="book-delete-alt"),
]