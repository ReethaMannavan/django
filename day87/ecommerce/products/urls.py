from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # homepage
    path('order/', views.place_order, name='place_order'),
    path('success/<int:order_id>/', views.order_success, name='order_success'),
    path('query/', views.customer_query, name='customer_query'),
    path('query/success/', views.query_success, name='query_success'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
