from rest_framework import viewsets, serializers
from rest_framework.response import Response
from rest_framework import status
from .models import Restaurant, Category, MenuItem
from .serializers import RestaurantSerializer, CategorySerializer, MenuItemSerializer
from rest_framework.decorators import action

# ReadOnly for Category
class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all()
    serializer_class = RestaurantSerializer


# Custom MenuItemViewSet with filtering logic
class MenuItemViewSet(viewsets.ModelViewSet):
    serializer_class = MenuItemSerializer

    def get_queryset(self):
        queryset = MenuItem.objects.all()
        restaurant_id = self.kwargs.get('restaurant_pk')
        if restaurant_id:
            queryset = queryset.filter(restaurant_id=restaurant_id)
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        return queryset

    def perform_create(self, serializer):
        restaurant_id = self.kwargs.get('restaurant_pk')
        if not restaurant_id:
            raise serializers.ValidationError({"restaurant": "Restaurant ID is required in URL."})
        serializer.save(restaurant_id=restaurant_id)
