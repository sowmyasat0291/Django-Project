# forms.py
from django import forms
from .models import Cart, CartItem

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = []  # No fields are needed because `Cart` is linked to `User`

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['cart', 'product', 'quantity']
        widgets = {
            'cart': forms.HiddenInput(),
            'product': forms.HiddenInput(),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
        }
