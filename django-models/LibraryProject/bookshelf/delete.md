## Delete a Book

<!-- First, import the `Book` model: -->
```python
from bookshelf.models import Book

# Command to delete the book:
book.delete()
books = Book.objects.all()
books

# Expected output:
<QuerySet []>