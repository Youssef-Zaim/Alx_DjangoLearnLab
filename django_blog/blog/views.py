from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, PostForm, CommentForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import Post, Comment
from django.urls import reverse_lazy
from taggit.models import Tag
from django.db.models import Q

# Registration view
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'blog/register.html', {'form':form})

# Logout view
def logout(request):
    logout(request)
    return redirect('login') 

# Profile management
@login_required
def profile(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserChangeForm(instance=request.user)
    return render(request, 'blog/profile.html', {'form': form})  

def blog(request):
    pass             

# List all the posts(public)
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    ordering = ['-published_date']
    paginate_by = 5
    
# View a single post
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    success_url = reverse_lazy('post-list') 
    
    
# Create a post(only logged in users)
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    
    # Automatically set the author
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
# Update a post (only author)
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'

    # Check if current user is the author
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author    

# Delete a post (only author)
class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  
    
# Comment Views
# Create a new comment for a post
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_pk = self.kwargs['post_pk']
        form.instance.author = self.request.user
        form.instance.post_id = post_pk
        return super().form_valid(form)
    
# Update comment (only author)
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author 
    
# Delete comment (only author)
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

    def get_success_url(self):
        # Redirect to the post detail page after deletion
        return self.object.post.get_absolute_url()   
    
class PostByTagListView(ListView):
    model = Post
    template_name = 'blog/posts_by_tag.html'
    context_object_name = 'posts'

    def get_queryset(self):
        tag_slug = self.kwargs['tag_slug']
        return Post.objects.filter(tags__slug__iexact=tag_slug).order_by('-published_date')          
    
class PostSearchListView(ListView):
    model = Post
    template_name = 'blog/search_results.html'
    context_object_name = 'posts'

    def get_queryset(self):
        query = self.request.GET.get('q')
        if query:
            return Post.objects.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query) | 
                Q(tags__name__icontains=query)
            ).distinct().order_by('-published_date')
        return Post.objects.none()       