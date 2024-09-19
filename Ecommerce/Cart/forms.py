from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from Cart.models import Cart, CartItem

class Cart(UserCreationForm):
    class Meta:
        model = Cart
        fields = ['user']
        widgets = {
            'user': forms.HiddenInput()
        }
class CartItem(UserCreationForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']
        widgets = {
            'cart': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput()
        }