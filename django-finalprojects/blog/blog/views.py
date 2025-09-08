from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .models import Post, Comment, Category
from .forms import CommentForm, BlogSearchForm, CustomUserCreationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.contrib.auth import login



# Blog list with search and filter
from django.views.generic import ListView
from django.db.models import Q, Count
from .models import Post, Category
from .forms import BlogSearchForm

class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 2

    def get_queryset(self):
        qs = super().get_queryset().order_by('-created_at')
        q = self.request.GET.get('q', '').strip()
        category_id = self.request.GET.get('category', '').strip()

        # Text search
        if q:
            qs = qs.filter(Q(title__icontains=q) | Q(content__icontains=q))

        # Category filter
        if category_id:
            try:
                category_id = int(category_id)
                qs = qs.filter(categories__id=category_id)
            except ValueError:
                pass  # ignore invalid category_id

        return qs.distinct()

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['search_form'] = BlogSearchForm(self.request.GET or None)
        # Only categories with posts in the filtered queryset
        ctx['categories'] = Category.objects.filter(posts__in=self.get_queryset()).distinct()
        return ctx



# Blog detail with comments
class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['comment_form'] = CommentForm()
        ctx['comments'] = self.object.comments.all().order_by('-created_at')
        return ctx

# Create post
class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content','image','categories']
    template_name = 'blog/post_form.html'

    def form_valid(self, form):
        form.instance.author = self.request.user
        messages.success(self.request, "Post created successfully!")
        return super().form_valid(form)

# Update/Delete Post - only author
class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title','content','image','categories']
    template_name = 'blog/post_form.html'

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

    def form_valid(self, form):
        messages.success(self.request, "Post updated successfully!")
        return super().form_valid(form)

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('blog:post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

# Add comment
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.contrib import messages
from .models import Comment, Post
from .forms import CommentForm

class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'blog/comment_form.html'

    def form_valid(self, form):
        post_pk = self.kwargs.get('post_pk')
        post = Post.objects.get(pk=post_pk)
        form.instance.post = post
        form.instance.user = self.request.user
        messages.success(self.request, "Comment added!")
        return super().form_valid(form)

    def get_success_url(self):
        return self.object.post.get_absolute_url()


# Edit/Delete comment
class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    fields = ['text']
    template_name = 'blog/comment_form.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def form_valid(self, form):
        messages.success(self.request, "Comment updated!")
        return super().form_valid(form)

class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'blog/comment_confirm_delete.html'

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.user

    def get_success_url(self):
        return self.object.post.get_absolute_url()


# blog/views.py
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # auto login
            return redirect('blog:post_list')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
