from django.db import models

# Author model
class Author(models.Model):
    """
    Author represents a single writer.
    - name: Human-readable name of the author.
    The reverse relation to Book is exposed as `books`.
    """
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name

# Book model
class Book(models.Model):
    """
    Book represents a single published work.
    - title: Title of the book.
    - publication_year: Year (YYYY) the book was published.
    - author: One-to-many link to Author. Many Books can belong to one Author.
      We set related_name='books' so Author.books gives us all related books.
    """
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    
    
    def __str__(self):
        return f"{self.title} ({self.publication_year}) by {self.author.name}"