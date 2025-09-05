# reviews/views.py
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.mail import send_mail
from django.db.models import Q, Avg, Count
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from .forms import SearchForm, ReviewForm, RegisterForm, LoginForm
from .models import Book, Review, Category

# ---------- Auth ----------
def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, "Registration successful. Welcome!")
            login(request, user)
            return redirect("book_list")
    else:
        form = RegisterForm()
    return render(request, "reviews/register.html", {"form": form})

def login_view(request):
    form = LoginForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        messages.success(request, "Logged in successfully.")
        return redirect("book_list")
    return render(request, "reviews/login.html", {"form": form})

from django.views.decorators.http import require_POST

@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "Logged out.")
    return redirect("book_list")

# ---------- Books ----------
class BookListView(ListView):
    model = Book
    template_name = "reviews/book_list.html"
    context_object_name = "books"
    paginate_by = 8

    def get_queryset(self):
        qs = Book.objects.all().annotate(
            avg_rating=Avg("reviews__rating"),
            review_count=Count("reviews")
        ).select_related()
        q = self.request.GET.get("q") or ""
        category_id = self.request.GET.get("category")
        if q:
            qs = qs.filter(Q(title__icontains=q))
        if category_id:
            qs = qs.filter(categories__id=category_id)
        return qs

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["search_form"] = SearchForm(self.request.GET or None)
        ctx["categories"] = Category.objects.all()
        ctx["active_category"] = self.request.GET.get("category") or ""
        return ctx

class BookDetailView(DetailView):
    model = Book
    template_name = "reviews/book_detail.html"
    context_object_name = "book"

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        book = self.object
        ctx["reviews"] = book.reviews.select_related("user").all()
        ctx["avg_rating"] = book.reviews.aggregate(Avg("rating"))["rating__avg"]
        return ctx

# ---------- Reviews ----------
class ReviewDetailView(DetailView):
    model = Review
    template_name = "reviews/review_detail.html"
    context_object_name = "review"

class ReviewCreateView(LoginRequiredMixin, CreateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def dispatch(self, request, *args, **kwargs):
        # Ensure book exists (explicit get_object_or_404 usage)
        self.book = get_object_or_404(Book, pk=kwargs.get("book_id"))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.book = self.book
        response = super().form_valid(form)
        # Email notify (admin)
        try:
            send_mail(
                subject=f"New Review: {self.book.title}",
                message=(
                    f"User: {self.request.user.username}\n"
                    f"Rating: {form.instance.rating}\n\n"
                    f"Comment:\n{form.instance.comment}"
                ),
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[settings.EMAIL_HOST_USER],
                fail_silently=False,
            )
        except Exception:
            # don't crash on email issues
            pass
        messages.success(self.request, "Review added successfully.")
        return response

    def get_success_url(self):
        return reverse("book_detail", args=[self.book.pk])

class ReviewUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Review
    form_class = ReviewForm
    template_name = "reviews/review_form.html"

    def get_object(self, queryset=None):
        # explicit get_object_or_404 usage
        return get_object_or_404(Review, pk=self.kwargs["pk"])

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user  # only owner can edit

    def handle_no_permission(self):
        messages.error(self.request, "You can only edit your own review.")
        return redirect("book_detail", pk=self.get_object().book.pk)

    def get_success_url(self):
        return reverse("book_detail", args=[self.object.book.pk])

class ReviewDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Review
    template_name = "reviews/review_confirm_delete.html"

    def get_object(self, queryset=None):
        return get_object_or_404(Review, pk=self.kwargs["pk"])

    def test_func(self):
        obj = self.get_object()
        # staff can delete any review; users can delete their own
        return self.request.user.is_staff or obj.user == self.request.user

    def handle_no_permission(self):
        messages.error(self.request, "You don't have permission to delete this review.")
        return redirect("book_detail", pk=self.get_object().book.pk)

    def get_success_url(self):
        messages.success(self.request, "Review deleted.")
        return reverse("book_detail", args=[self.object.book.pk])
