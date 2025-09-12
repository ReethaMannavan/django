from rest_framework.routers import DefaultRouter
from rest_framework_nested.routers import NestedDefaultRouter
from .views import RestaurantViewSet, CategoryViewSet, MenuItemViewSet

# Main router
router = DefaultRouter()
router.register(r'restaurants', RestaurantViewSet)
router.register(r'categories', CategoryViewSet, basename='category')

# Nested router for menu items under restaurants
restaurants_router = NestedDefaultRouter(router, r'restaurants', lookup='restaurant')
restaurants_router.register(r'menu-items', MenuItemViewSet, basename='restaurant-menu-items')

urlpatterns = router.urls + restaurants_router.urls
