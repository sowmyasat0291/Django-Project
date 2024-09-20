from django.urls import path
from .views import index_view, signup_view, login_view, product_list, cart_view, logout_view

urlpatterns = [
    path('', index_view, name='index'),  # Redirects to login or product list
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('product/', product_list, name='product_list'),
    path('cart/', cart_view, name='cart'),  # Cart view
]
