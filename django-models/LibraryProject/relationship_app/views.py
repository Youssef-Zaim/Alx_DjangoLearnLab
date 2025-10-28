from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from .models import Book
from .models import Library
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .models import UserProfile
from .forms import BookForm
from django.contrib.auth.decorators import permission_required

# Function to list all books
def list_books(request):
    # Fetch all books from the database
    books = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'book': books})


# class-based view to display details for a specific library
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'
    
    
# Function to handle user registration
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})


# Function to handle user login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('list_books')
        else:
            return render(request, 'relationship_app/login.html', {'error': 'Invalid credentials'})
    return render(request, 'relationship_app/login.html')

# Function to handle user logout
@login_required
def user_logout(request):
    logout(request)
    return redirect('login')



# Role Based Access Control
# Function to check if user is an admin
def is_admin(user):
    return user.profile.roles == 'Admin'

# Function to check if user is a librarian
def is_librarian(user):
    return user.profile.roles == 'Librarian'  

# Function to check if user is a member
def is_member(user):
    return user.profile.roles == 'Member'


# Views for role-based access control
# Admin view, accessible only by Admin users
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

# Librarian view, accessible only by Librarian users
@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

# Member view, accessible only by Member users
@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')



# Views for book permissions
# View to add a book
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})   

# View to change a book
@permission_required('relationship_app.can_change_book', raise_exception=True)
def change_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('list_books')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/change_book.html', {'form': form, 'book': book})   

# View to delete a book
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        book.delete()
        return redirect('list_books')
    return render(request, 'relationship_app/delete_book.html', {'book': book})  
