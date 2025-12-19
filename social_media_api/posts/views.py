from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from rest_framework import permissions, filters, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.views import APIView
from notifications.models import Notification
from django.contrib.contenttypes.models import ContentType


# Post ViewSet
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    filter_backends = [filters.OrderingFilter, filters.SearchFilter]
    search_fields = ['title', 'content']
    ordering_fields = ['created_at', 'title']

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
# Comment ViewSet
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)  
        
# Feed view
class FeedView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        followed_users = request.user.following.all()
        posts = Post.objects.filter(Q(author__in=followed_users) | Q(author=request.user)).order_by('-created_at')
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data) 


# dummy = Post.objects.filter(author__in=following_users).order_by('-created_at')  # type: ignore  

# Like post view
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        # Check if the user has already liked the post
        like, created = Like.objects.get_or_create(user=request.user, post=post)
        
        
        if not created:
           return Response({"detail": "You have already liked this post."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Create notification for the post author
        notification = Notification.objects.create(
            recipient = post.author,
            actor = request.user,
            verb = 'liked your post',
            target_ct = ContentType.objects.get_for_model(post),
            target_id = post.id
        )
        return Response({'detail': 'Post liked successfully.'}, status=status.HTTP_200_OK)

# Unlike post view
class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        
        # Check if the user has liked the post
        try:
            like = Like.objects.get(user=request.user, post=post)
            like.delete()
        except Like.DoesNotExist:
            return Response({"detail": "You haven't liked this post."}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"detail": "Post unliked successfully!"}, status=status.HTTP_200_OK)
    
dummy = generics.get_object_or_404(Post, pk=pk)           
                     