#cart/urls.py
from django.urls import path
from .views import add_to_cart, cart_detail, remove_from_cart, update_cart_item, checkout_view, checkout_success, checkout_cancel

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),  # Add item to cart
    path('', cart_detail, name='cart_detail'),  # View cart
    path('remove/<int:item_id>/', remove_from_cart, name='cart_remove'),
    path('update/<int:item_id>/', update_cart_item, name='update_cart_item'),  # Update cart item
    path('checkout/', checkout_view, name='checkout'),
    path('checkout/success/', checkout_success, name='checkout_success'),
    path('checkout/cancel/', checkout_cancel, name='checkout_cancel'),
]
