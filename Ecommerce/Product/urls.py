from django.urls import path, include
from django.contrib.auth.views import LogoutView
from .views import signup_view, login_view,  product_list, ProductListCreateView, ProductDetailView
urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('product/', product_list, name='product_list'),
    path('api/products/', ProductListCreateView.as_view(), name='product_list_create'),
    path('api/products/<int:pk>/', ProductDetailView.as_view(), name='product_detail'),
]





    

