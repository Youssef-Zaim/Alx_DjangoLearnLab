## Update a Book

Command to update the title of the book "1984" to "Nineteen Eighty-Four":
```python
book = Book.objects.get(title="1984")
book.title = "Nineteen Eighty-Four"
book.save()
book

# Expected output:
<Book: Nineteen Eighty-Four>