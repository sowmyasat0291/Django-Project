from django.db import models
from Product.models import Product
from django.contrib.auth.models import User

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Link to User
    product = models.ForeignKey(Product, on_delete=models.CASCADE)  # Link to Product
    quantity = models.PositiveIntegerField(default=1)  # Product quantity
    created_at = models.DateTimeField(auto_now_add=True, null=True)  # Cart creation time

    def __str__(self):
        return f"{self.quantity}x {self.product.name} in {self.user.username}'s cart"
