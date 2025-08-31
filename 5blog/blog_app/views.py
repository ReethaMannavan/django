from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from django.urls import reverse_lazy

from .models import Post, Comment
from .forms import PostForm, CommentForm

# CBV: List all posts
class PostListView(ListView):
    model = Post
    template_name = 'blog_app/post_list.html'
    context_object_name = 'posts'
    paginate_by = 5

# CBV: Post detail + comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog_app/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'

# FBV: Create new post
@login_required
def post_create(request):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, "Post created successfully!")
            return redirect('blog_app:post_detail', slug=post.slug)
    else:
        form = PostForm()
    return render(request, 'blog_app/post_form.html', {'form': form})

# FBV: Add comment
@login_required
def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                post=post,
                user=request.user,
                text=form.cleaned_data['text']
            )
            messages.success(request, "Comment added!")
            return redirect('blog_app:post_detail', slug=slug)
    else:
        form = CommentForm()
    return render(request, 'blog_app/comment_form.html', {'form': form, 'post': post})

# CBV: Delete comment
class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog_app/comment_confirm_delete.html"

    def get_success_url(self):
        return self.object.post.get_absolute_url()

    def test_func(self):
        return self.request.user == self.get_object().user

# FBV: User registration
def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('blog_app:post_list')
    else:
        form = UserCreationForm()
    return render(request, "blog_app/register.html", {"form": form})
