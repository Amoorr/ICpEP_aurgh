"""
admin.py is simply a display for the admin interface (or superuser rather). This is just for
developers.
"""

from django.contrib import admin
from .models import Product, Cart

# Admin model for Product
class ProductAdmin(admin.ModelAdmin):
    list_display = ('product_name', 'price', 'quantity', 'tag')
    search_fields = ('product_name', 'tag')  # Allow searching by product name and tag
    list_filter = ('tag',)  # Filter products by tag
    ordering = ('product_name',)  # Default ordering by product name

    # Fields that should be displayed when adding/editing products
    fields = ('product_name', 'price', 'tag', 'quantity')

    # Optional: Display a custom message after saving a product
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        # You can add custom behavior here, like logging or sending notifications

# Admin model for Cart
class CartAdmin(admin.ModelAdmin):
    list_display = ('cart_id', 'user', 'product', 'quantity', 'order_status', 'order_date')
    search_fields = ('user__email', 'product__product_name')  # Searching by user email and product name
    list_filter = ('order_status', 'order_date')  # Filter by order status and order date
    ordering = ('order_date',)  # Default ordering by order date
    
    # Optional: Display total price in the list view (calculated dynamically)
    def total_price(self, obj):
        return obj.quantity * obj.product.price
    total_price.short_description = 'Total Price'  # Change column name to "Total Price"
    
    # Optional: Make the total price column visible in the list view
    list_display = ('cart_id', 'user', 'product', 'quantity', 'order_status', 'order_date', 'total_price')

# Register models with Django Admin
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
