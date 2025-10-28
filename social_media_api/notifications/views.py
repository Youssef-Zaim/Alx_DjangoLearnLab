from .models import Notification
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response

# Notification list view
class NotificationListView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        notifications = Notification.objects.filter(recipient=request.user).order_by('-timestamp')
        notification_data = [{"actor": notification.actor.username, "verb": notification.verb, "target": str(notification.target), "timestamp": notification.timestamp} for notification in notifications]
        return Response(notification_data, status=status.HTTP_200_OK)
