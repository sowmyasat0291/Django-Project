# views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Cart, CartItem
from Product.models import Product

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Ensure one cart per user

    # Try to get the existing cart item or create a new one
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # Increment quantity for existing item
        cart_item.save()

    return redirect('cart_detail')  # Ensure this URL is defined


@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)  # Get the user's cart
    items = cart.items.all()  # Fetch items in the cart

    total_amount = sum(item.quantity * item.product.price for item in items)  # Calculate total amount

    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total_amount': total_amount,
    })  # Render the cart detail template


@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)  # Get the user's cart
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)  # Get specific item
    cart_item.delete()  # Remove the item from the cart
    return redirect('cart_detail')  # Redirect to cart detail after removal
