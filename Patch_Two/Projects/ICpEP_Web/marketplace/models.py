from django.db import models
from accounts.models import CustomUser
from django.core.exceptions import ValidationError
from django.db import transaction

class Product(models.Model):
    """
    Represents products available in the marketplace.
    Tracks stock (quantity) and additional product details.
    """
    TAG_CHOICES = [
        ('Pre-orderable', 'Pre-orderable'),
        ('Buyable', 'Buyable'),
    ]
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    tag = models.CharField(max_length=200, blank=True, null=True)  # Tags can be optional
    quantity = models.IntegerField(default=0)  # Tracks available stock
    pre_order = models.BooleanField(default=False)  # Indicates if the product is pre-orderable
    product_description = models.TextField(blank=True, null=True)  # New field for product description

    def __str__(self):
        return self.product_name

    def is_stock_available(self, order_quantity):
        """
        Checks if sufficient stock is available for an order.
        Allows pre-orderable products even if stock is 0.
        """
        if self.tag == 'Pre-orderable':
            return True  # Pre-orderable items can always be "ordered"
        return self.quantity >= order_quantity

    def reduce_stock(self, order_quantity):
        """
        Reduces stock quantity after a successful order.
        Uses transaction to ensure atomicity.
        """
        if self.is_stock_available(order_quantity):
            with transaction.atomic():
                self.quantity -= order_quantity
                self.save()
                return True
        return False

    class Meta:
        db_table = 'Product'  # Custom table name
        ordering = ['product_name']  # Default ordering by product name


class Cart(models.Model):
    """
    Represents a user's cart containing their orders.
    Tracks the user, product, quantity, order status, and date of the order.
    """
    cart_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='carts')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='carts')
    quantity = models.IntegerField(default=0)  # Quantity ordered
    order_status = models.CharField(
        max_length=20,
        choices=[
            ('Pending', 'Pending'),
            ('Received', 'Received'),
            ('Cancelled', 'Cancelled')  # Added status for cancellations
        ],
        default='Pending'
    )
    order_date = models.DateField(auto_now_add=True)  # Automatically set the order date

    def __str__(self):
        return f'Cart {self.cart_id} for {self.user}'

    def total_price(self):
        """
        Calculates the total price of the cart item.
        """
        return self.product.price * self.quantity

    def clean(self):
        """
        Ensures the quantity is greater than zero.
        """
        if self.quantity <= 0:
            raise ValidationError('Quantity must be greater than zero.')

    class Meta:
        db_table = 'Cart'
        ordering = ['order_date']  # Default ordering by order date


class ProductImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')  # Foreign key to Product
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)  # Made image optional

    def __str__(self):
        return f"Image for {self.product.product_name}"

    class Meta:
        db_table = 'ProductImage'
        ordering = ['image_id']
