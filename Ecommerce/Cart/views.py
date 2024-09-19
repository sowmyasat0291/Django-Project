from django.shortcuts import render, redirect
from .models import Cart, CartItem
from Product.models import Product
from django.contrib.auth.decorators import login_required

@login_required
def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart = Cart.objects.get(user=request.user)
    return render(request, 'cart/cart_detail.html', {'cart': cart})

