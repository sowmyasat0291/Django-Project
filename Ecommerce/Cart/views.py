from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Cart, CartItem
from Product.models import Product

@login_required
def cart_add(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    cart, created = Cart.objects.get_or_create(user=request.user)  # Ensure one cart per user
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1
        cart_item.save()  # Increment quantity for existing item

    return redirect('cart_detail')  # Ensure this URL is defined

@login_required
def cart_detail(request):
    cart = get_object_or_404(Cart, user=request.user)  # Get the user's cart
    items = CartItem.objects.filter(cart=cart)  # Fetch items in the cart

    valid_items = []
    for item in items:
        try:
            product = item.product  # Accessing the product relationship
            valid_items.append(item)
        except Product.DoesNotExist:
            # Handle the case where the product does not exist
            item.delete()  # Remove the item if the product is gone

    return render(request, 'cart/cart_detail.html', {'items': valid_items})  # Render the cart detail template

@login_required
def cart_remove(request, product_id):
    cart = get_object_or_404(Cart, user=request.user)  # Get the user's cart
    cart_item = get_object_or_404(CartItem, cart=cart, product_id=product_id)  # Get specific item
    cart_item.delete()  # Remove the item from the cart
    return redirect('cart_detail')  # Redirect to cart detail after removal
@receiver(post_delete, sender=Product)
def delete_cart_items(sender, instance, **kwargs):
    CartItem.objects.filter(product=instance).delete()
