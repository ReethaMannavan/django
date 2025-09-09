from rest_framework import serializers
from .models import Book, Author
from datetime import date

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = "__all__"

class BookSerializer(serializers.ModelSerializer):
    book_age = serializers.SerializerMethodField()
    author = AuthorSerializer(read_only=True)
    author_id = serializers.PrimaryKeyRelatedField(
        queryset=Author.objects.all(), source="author", write_only=True
    )

    class Meta:
        model = Book
        fields = ["id", "title", "published_year", "author", "author_id", "book_age"]

    def get_book_age(self, obj):
        return date.today().year - obj.published_year

    def validate_published_year(self, value):
        if value > date.today().year:
            raise serializers.ValidationError("Published year cannot be in the future.")
        return value
