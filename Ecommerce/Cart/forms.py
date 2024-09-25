from django import forms
from .models import CartItem

class CartItemForm(forms.ModelForm):
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']  # Specify the fields you want in the form
        widgets = {
            'product': forms.HiddenInput(),  # Hide the product field in the form
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),  # Display quantity as a number input
        }
