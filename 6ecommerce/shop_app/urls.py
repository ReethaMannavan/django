from django.urls import path
from . import views

app_name = "shop_app"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product_list"),
    path("product/<int:pk>/", views.ProductDetailView.as_view(), name="product_detail"),
    path("register/", views.register, name="register"),
    path("cart/", views.cart_view, name="cart"),
    path("add-to-cart/<int:pk>/", views.add_to_cart, name="add_to_cart"),
    path("remove-from-cart/<int:pk>/", views.remove_from_cart, name="remove_from_cart"),
]
