from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import LimitOffsetPagination
from .models import Movie, Review, Genre
from .serializers import MovieSerializer, ReviewSerializer, GenreSerializer
from .filters import ReviewFilter


class MoviePagination(LimitOffsetPagination):
    default_limit = 5
    max_limit = 20


class MovieViewSet(viewsets.ModelViewSet):
    queryset = Movie.objects.all().order_by("id")
    serializer_class = MovieSerializer
    pagination_class = MoviePagination
    filter_backends = [filters.SearchFilter]
    search_fields = ["title", "actors"]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all().order_by("-created_at")
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = ReviewFilter
    ordering_fields = ["rating", "created_at"]


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
