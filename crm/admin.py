"""
Admin configuration for CRM models.
"""
from django.contrib import admin
from .models import Customer, Order


@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    """Admin interface for Customer model."""
    list_display = ['name', 'email', 'created_at']
    search_fields = ['name', 'email']
    list_filter = ['created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin interface for Order model."""
    list_display = ['id', 'customer', 'total_amount', 'created_at']
    list_filter = ['created_at']
    search_fields = ['customer__name', 'customer__email']

