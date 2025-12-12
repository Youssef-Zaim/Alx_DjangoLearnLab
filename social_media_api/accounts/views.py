# accounts/views.py
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, parser_classes
from rest_framework.parsers import MultiPartParser, FormParser
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from .serializers import RegisterSerializer, UserSerializer, UserProfileSerializer

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    """
    POST /register/
    بيانات: username, email, password, password2, (bio), (profile_picture)
    """
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [MultiPartParser, FormParser]  # support file upload (profile_picture)


class LoginTokenView(TokenObtainPairView):
    """
    POST /login/  (delegates to simplejwt TokenObtainPairView)
    body: { "username": "...", "password": "..." }
    returns: { "access": "...", "refresh": "..." }
    """
    permission_classes = [permissions.AllowAny]


class ProfileView(generics.RetrieveUpdateAPIView):
    """
    GET /profile/  -> returns current user's profile
    PATCH /profile/ -> update fields (bio, profile_picture)
    Requires Authorization: Bearer <access_token>
    """
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user


@api_view(["POST"])
@permission_classes([permissions.IsAuthenticated])
def follow_toggle(request, username):
    """
    POST /follow/<username>/
    Toggle follow/unfollow the target user.
    Returns JSON with detail: "followed" or "unfollowed".
    """
    try:
        target = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({"detail": "User not found."}, status=status.HTTP_404_NOT_FOUND)

    user = request.user
    if user == target:
        return Response({"detail": "Cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)

    if target.followers.filter(id=user.id).exists():
        target.followers.remove(user)
        return Response({"detail": "unfollowed"}, status=status.HTTP_200_OK)
    else:
        target.followers.add(user)
        return Response({"detail": "followed"}, status=status.HTTP_200_OK)
