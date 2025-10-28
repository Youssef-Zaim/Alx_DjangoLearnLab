from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from .models import BlogPost
from .forms import BlogPostForm
from django.contrib import messages
from .models import Book
from django.http import HttpResponse
from .forms import BookForm
from django.core.paginator import Paginator
from .forms import ExampleForm

# View to display a form to demonstrate security features
def my_view(request):
    if request.method == 'POST':
        # Use Django forms for validation and security
        form = BookForm(request.POST)
        if form.is_valid():
            # Safe to process the data, as it's validated
            form.save()  # Assuming BookForm is tied to a Book model
            return HttpResponse('Form submitted successfully!')
        else:
            return HttpResponse('Form is not valid')
    else:
        form = BookForm()  # Empty form when GET request
    return render(request, 'bookshelf/form_example.html', {'form': form})

# View to display a list of all books
def book_list(request):
    books = Book.objects.all()
    
    # Paginate results
    paginator = Paginator(books, 10)  # Show 10 books per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'bookshelf/book_list.html', {'page_obj': page_obj})

# View to display details of a single book
def book_detail(request, pk):
    # Use get_object_or_404 to avoid SQL injection and ensure the book exists
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'bookshelf/book_detail.html', {'book': book})

# View to create a new blog post
@permission_required('blog.can_create', raise_exception=True)
def create_blog_post(request):
    if request.method == 'POST':
        form = BlogPostForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Blog post created successfully!")
            return redirect('blog:post_list')
    else:
        form = BlogPostForm()
    return render(request, 'blog/create_post.html', {'form': form})

# View to edit an existing blog post
@permission_required('blog.can_edit', raise_exception=True)
def edit_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    if request.method == 'POST':
        form = BlogPostForm(request.POST, instance=blog_post)
        if form.is_valid():
            form.save()
            return redirect('blog:post_detail', pk=blog_post.pk)
    else:
        form = BlogPostForm(instance=blog_post)
    return render(request, 'blog/edit_post.html', {'form': form, 'blog_post': blog_post})

# view to delete a blog post
@permission_required('blog.can_delete', raise_exception=True)
def delete_blog_post(request, pk):
    blog_post = get_object_or_404(BlogPost, pk=pk)
    blog_post.delete()
    return redirect('blog:post_list')     

# View to view a blog post (for viewers)
@permission_required('blog.can_view', raise_exception=True)
def view_blog_post(request, pk):
     blog_post = get_object_or_404(BlogPost, pk=pk)
     return render(request, 'blog/view_post.html', {'blog_post': blog_post})