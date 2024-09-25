from django.urls import path
from .views import cart_add, cart_detail, cart_remove

urlpatterns = [
    path('cart/add/<int:product_id>/', cart_add, name='add_to_cart'),
    path('cart/', cart_detail, name='cart_detail'),
    path('cart/remove/<int:product_id>/', cart_remove, name='remove_from_cart'),
]
