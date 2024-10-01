from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from Product.models import Product

@login_required
def add_to_cart(request, product_id):
    if request.user.groups.filter(name='Buyer').exists():  # Only buyers can add to cart
        product = get_object_or_404(Product, id=product_id)
        cart, _ = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1  # Increment quantity if the item is already in the cart
        cart_item.save()
        messages.success(request, 'Item added to cart successfully.')
        return redirect('product_list')  # Redirect to product list or cart view as needed

    messages.error(request, 'You do not have permission to add items to the cart.')
    return redirect('product_list')


@login_required
def update_cart_item(request, item_id):
    if request.user.groups.filter(name='Buyer').exists():  # Only buyers can update cart items
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if quantity and quantity.isdigit() and int(quantity) > 0:  # Ensure quantity is valid
                cart_item.quantity = int(quantity)  # Update quantity
                cart_item.save()
                messages.success(request, 'Cart item updated successfully.')
            else:
                messages.error(request, 'Invalid quantity.')
            return redirect('cart_detail')

    messages.error(request, 'You do not have permission to update cart items.')
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    if request.user.groups.filter(name='Buyer').exists():  # Only buyers can remove items
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully.')
        return redirect('cart_detail')

    messages.error(request, 'You do not have permission to remove items from the cart.')
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    if request.user.groups.filter(name='Seller').exists():  # If the user is a seller
        items = CartItem.objects.all()  # Show all cart items across all users
    else:
        cart = get_object_or_404(Cart, user=request.user)  # Get the buyer's cart
        items = cart.items.all()  # Get the items in the buyer's cart

    total_amount = sum(item.quantity * item.product.price for item in items)

    return render(request, 'cart/cart_detail.html', {
        'items': items,
        'total_amount': total_amount,
    })
