from django.db import models
from Product.models import Product  # Make sure this import is correct

class Cart(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='cart_items', on_delete=models.CASCADE)  # Correctly reference the Product model
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product.name} (x{self.quantity})"
