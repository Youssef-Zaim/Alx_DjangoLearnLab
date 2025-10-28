## Retrieve a Book

<!-- Command to retrieve all books: -->
```python
books = Book.objects.get()
books

# Expected output:
<QuerySet [<Book: 1984>]>