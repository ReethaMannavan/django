import django_filters
from .models import Book

class BookFilter(django_filters.FilterSet):
    price_min = django_filters.NumberFilter(field_name="price", lookup_expr="gte")
    price_max = django_filters.NumberFilter(field_name="price", lookup_expr="lte")
    author = django_filters.CharFilter(field_name="author__name", lookup_expr="icontains")
    category = django_filters.CharFilter(field_name="category__name", lookup_expr="icontains")

    class Meta:
        model = Book
        fields = ["price_min", "price_max", "author", "category"]
