from django import forms
from .models import Cart

class CartForm(forms.ModelForm):
    class Meta:
        model = Cart
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.HiddenInput(),  # Hide the product field
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),  # Display quantity field as a number input
        }
