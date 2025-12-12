# accounts/urls.py
from django.urls import path
from .views import RegisterView, LoginTokenView, ProfileView, follow_toggle
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Registration & Login (JWT)
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginTokenView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Profile
    path('profile/', ProfileView.as_view(), name='profile'),

    # Follow / Unfollow (toggle)
    path('follow/<str:username>/', follow_toggle, name='follow-toggle'),
]
