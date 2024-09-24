from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Product.models import Product  # Adjust the import path as necessary
from Cart.models import Cart, CartItem

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)
    
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()  # Save whether the item is created or updated
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)
    cart_item.delete()
    
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart = get_object_or_404(Cart, user=request.user)  # Get the cart for the logged-in user
    cart_items = CartItem.objects.filter(cart=cart)  # Get all cart items for this user's cart
    
    for item in cart_items:
        item.total = item.product.price * item.quantity  # Calculate the total for each item
    
    total_amount = sum(item.total for item in cart_items)  # Calculate the total cart amount
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart/cart.html', context)  # Adjust the template path if necessary
