from django.contrib import admin
from .models import Order, CustomerQuery

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user', 'total_amount', 'created_at')

@admin.register(CustomerQuery)
class CustomerQueryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'user', 'created_at')
