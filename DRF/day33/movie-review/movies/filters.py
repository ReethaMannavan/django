import django_filters
from .models import Review


class ReviewFilter(django_filters.FilterSet):
    movie = django_filters.CharFilter(field_name="movie__title", lookup_expr="icontains")
    reviewer = django_filters.CharFilter(field_name="reviewer", lookup_expr="icontains")
    rating = django_filters.NumberFilter(field_name="rating")

    class Meta:
        model = Review
        fields = ["movie", "reviewer", "rating"]
