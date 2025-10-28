import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    """
      Filter set for exposing commom filters for book.
      - title: case-insensitive contains
      - author: by author id (exact match)
      - author_name: case-insensitive contains on related Author.name
      - publication_year: exact year
      - year_min/year_max: inclusive numeric range for publication_year
    """
    title = django_filters.CharFilter(field_name="title", lookup_expr="icontains")
    author = django_filters.NumberFilter(field_name="author_id")
    author_name = django_filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    publication_year = django_filters.NumberFilter(field_name="publication_year", lookup_expr="exact")
    year_min = django_filters.NumberFilter(field_name="publication_year", lookup_expr="gte")
    year_max = django_filters.NumberFilter(field_name="publication_year", lookup_expr="lte")
    
    class Meta:
        model = Book
        # Expose friendly param names; django-filter will ignore unknowns
        fields = ["title", "author", "author_name", "publication_year", "year_min", "year_max"]