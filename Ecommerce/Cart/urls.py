from django.urls import path
from .views import add_to_cart, cart_detail

urlpatterns = [
    path('add/<int:product_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
]
