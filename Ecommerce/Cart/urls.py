# cart/urls.py
from django.urls import path
from .views import add_to_cart, remove_from_cart, view_cart

urlpatterns = [
    path('cart/add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/remove/<int:product_id>/', remove_from_cart, name='remove_from_cart'),
    path('cart/view/', view_cart, name='view_cart'),
]
