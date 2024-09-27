# cart/models.py

from django.db import models
from django.contrib.auth.models import User
from Product.models import Product

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Ensures one cart per user
    

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')  # Allows access to items from cart
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = (('cart', 'product'),)  # Ensure one product per cart

    def __str__(self):
        return f"{self.quantity} of {self.product.name} in cart"
