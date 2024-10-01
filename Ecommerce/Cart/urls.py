#cart/urls.py
from django.urls import path
from .views import add_to_cart, cart_detail, remove_from_cart, update_cart_item

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Add item to cart
    path('', cart_detail, name='cart_detail'),  # View cart
    path('remove/<int:item_id>/', remove_from_cart, name='cart_remove'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),  # Update cart item
]
