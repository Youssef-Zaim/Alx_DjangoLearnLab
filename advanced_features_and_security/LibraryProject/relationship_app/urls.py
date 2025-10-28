from django.urls import path
from .views import list_books, LibraryDetailView
from . import views
from django.contrib.auth.views import LoginView, LogoutView

urls_patterns = [
    path('books/', list_books, name='list_books'),
    path('add_book/', views.add_book, name='add_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    path('register/', views.register, name='register'),
    path('login/', LoginView.as_view(template_name='application_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='application_app/logout.html'), name='logout'),
    path('admin/', views.admin_view, name='admin_view'),
    path('librarian/', views.librarian_view, name='librarian_view'),
    path('member/', views.member_view, name='member_view'),  
]