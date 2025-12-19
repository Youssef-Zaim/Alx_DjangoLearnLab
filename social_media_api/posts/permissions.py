from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow authors of a post or comment to edit or delete them.
    """
    def has_object_permission(self, request, view, obj):
        # Allow read-only access for everyone
        if request.method in permissions.SAFE_METHODS:
            return True
        # Allow only authors to edit or delete
        return obj.author == request.user
