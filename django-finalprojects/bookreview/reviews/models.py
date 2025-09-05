# reviews/models.py
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator

def cover_upload_path(instance, filename):
    return f"covers/book_{instance.id or 'new'}/{filename}"

class Category(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=120)
    description = models.TextField(blank=True)
    cover_image = models.ImageField(upload_to=cover_upload_path, blank=True, null=True)
    categories = models.ManyToManyField(Category, related_name="books", blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["title"]

    def __str__(self):
        return f"{self.title} — {self.author}"

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        unique_together = ("book", "user")  # one review per user per book (optional but nice)

    def __str__(self):
        return f"{self.book.title} — {self.user.username} ({self.rating}/5)"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    # extend later (avatar, bio, etc.)

    def __str__(self):
        return f"{self.user.username}'s profile"
