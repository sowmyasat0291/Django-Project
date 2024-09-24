from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from Product.models import Product  # Adjust the import path as necessary
from Cart.models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
        cart_item.save()
    
    return redirect('cart')

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    
    return redirect('cart')

def view_cart(request):
    cart_items = CartItem.objects.filter(cart=request.session['cart_id'])  
    for item in cart_items:
        item.total = item.product.price * item.quantity
    
    total_amount = sum(item.total for item in cart_items)    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart.html')  