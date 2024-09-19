from django.urls import path, include
from .views import signup_view, login_view, product_list
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('signup/', signup_view, name='signup'),
    path('login/', login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('product/', product_list, name='product_list'),
    

]