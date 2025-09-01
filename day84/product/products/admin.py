from django.contrib import admin

# Register your models here.
# products/admin.py
from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'brand', 'price', 'is_available')
    list_filter = ('brand', 'is_available')
    search_fields = ('name', 'brand')
