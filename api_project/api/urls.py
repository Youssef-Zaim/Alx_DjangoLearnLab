from django.urls import path, include
from .views import BookList
from rest_framework.routers import DefaultRouter
from .views import BookViewSet
from rest_framework.authtoken import views as auth_views

# Router and registration for the BookViewSet
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    path('books/', BookList.as_view(), name='book-list'),  # URL for listing books
    path('', include(router.urls)),  # Include the router URLs for BookViewSet
    path('api-auth-token/', auth_views.obtain_auth_token, name='api_auth-token'),  # URL for token authentication
]