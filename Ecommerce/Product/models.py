from django.db import models
from django.utils import timezone

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.IntegerField(default=0)
    stock = models.IntegerField(default=0)  # Set default to 0
    description = models.TextField(blank=True)
    banner = models.ImageField(upload_to='images/',blank=True)
    
    def __str__(self):
        return self.name
