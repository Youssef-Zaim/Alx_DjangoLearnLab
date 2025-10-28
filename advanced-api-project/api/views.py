from  django.db import transaction
from django.db.models import Q
from rest_framework import generics, filters
from rest_framework.exceptions import ValidationError
from .models import Book
from .serializers import BookSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.authentication import BasicAuthentication 
from .filters import BookFilter
from django_filters import rest_framework


# Book List View and permissions
class BookListView(generics.ListAPIView):
    """
        Read-only endpoint listing books with rich query capabilities.

        Filtering (django-filter):
        - ?title=<substring>               (icontains on title)
        - ?author=<id>                     (exact author id)
        - ?author_name=<substring>         (icontains on Author.name)
        - ?publication_year=YYYY
        - ?year_min=YYYY&year_max=YYYY     (inclusive range)

        Search (DRF SearchFilter):
        - ?search=<text> over: title, author name

        Ordering (DRF OrderingFilter):
        - ?ordering=publication_year       (prefix with '-' for desc)
        - You can order by ANY model field (ordering_fields='__all__').

        Examples:
        /api/books/?author_name=toni&year_min=1970&year_max=1995&search=beloved&ordering=-publication_year
    """
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
     # Backends: django-filter + built-in search/ordering
    filter_backends = [
        rest_framework.DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = BookFilter
    
    # Search across title and related author name
    search_fields = ["title", "author__name"]
    
    # Allow ordering by any model field (title, publication_year, id, etc.)
    ordering_fields = "__all__"
    ordering = ["title"]
    
# Class for book detail view
class BookDetailView(generics.RetrieveAPIView):
    """
        Read-only view that returns a single book by primary key (id)
        Permissions:
        - AllowAny (public read)
    """  
    queryset = Book.objects.select_related("author").all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
# Class for book creation view
class BookCreateView(generics.CreateAPIView):
    """Create a new book
       Permissions:
       - Authenticated users only
       Customizations:
       - perform_create: wrap in a transaction and normalize title whitespace.
       - Additional server-side guard to ensure title isn't blank after stripping, complementing serializer validation.
    """
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]
    
    @transaction.atomic
    def perform_create(self, serializer):
        title = (self.request.data.get("title") or "").strip()
        if not title:
            raise ValidationError({"title": "Title cannot be blank."})
        serializer.save(title=title)
        
# Class for book update view
class BookUpdateView(generics.UpdateAPIView):
    """Update an existing book (PUT/PATCH)
       Permissions:
       - Authenticated users only
       Customizations:
       - Perform_update: normalize title, stay atomic.
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [BasicAuthentication]
    
    @transaction.atomic
    def perform_update(self, serializer):
        title = (self.request.data.get("title") or "").strip()
        if title == "":
            raise ValidationError({"title": "Title cannot be blank."})
        serializer.save(title=title if title else serializer.instance.title)
        
# Class for book delete view
class BookDeleteView(generics.DestroyAPIView):
    """Delete a book.
       Permissions:
       - Authenticated users only
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated] 
    authentication_classes = [BasicAuthentication]                                                        
    
