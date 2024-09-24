from django.urls import path
from .views import index_view, signup_view, login_view, logout_view, product_list, create_product, update_product, cart_view, delete_product

urlpatterns = [
    path('', index_view, name='index'), 
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('product/', product_list, name='product_list'),
    path('products/create/', create_product, name='create_product'),
    path('products/update/<int:pk>/', update_product, name='update_product'),
    path('products/delete/<int:pk>/', delete_product, name='delete_product'),
    path('cart/', cart_view, name='cart'),  # Cart view
]
