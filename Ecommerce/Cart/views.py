from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from Product.models import Product

@login_required
def add_to_cart(request, product_id, buyer_username=None):
    if request.user.groups.filter(name='Buyer').exists() or request.user.groups.filter(name__in=['Admin', 'Seller']).exists():
        product = get_object_or_404(Product, id=product_id)

        # If the logged-in user is an admin or seller, find the specified buyer's cart
        if request.user.groups.filter(name__in=['Admin', 'Seller']).exists() and buyer_username:
            buyer = get_object_or_404(User, username=buyer_username)
            cart, _ = Cart.objects.get_or_create(user=buyer)
        else:
            cart, _ = Cart.objects.get_or_create(user=request.user)  # Normal buyer cart

        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        if not created:
            cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Item added to cart successfully.')
        return redirect('product_list')

    messages.error(request, 'You do not have permission to add items to the cart.')
    return redirect('product_list')


@login_required
def update_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Allow admins and sellers to update any cart item
    if request.user.groups.filter(name__in=['Admin', 'Seller']).exists() or cart_item.cart.user == request.user:
        if request.method == 'POST':
            quantity = request.POST.get('quantity')
            if quantity and quantity.isdigit() and int(quantity) > 0:
                cart_item.quantity = int(quantity)
                cart_item.save()
                messages.success(request, 'Cart item updated successfully.')
            else:
                messages.error(request, 'Invalid quantity.')
            return redirect('cart_detail')

    messages.error(request, 'You do not have permission to update cart items.')
    return redirect('cart_detail')


@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)

    # Allow admins and sellers to remove any cart item
    if request.user.groups.filter(name__in=['Admin', 'Seller']).exists() or cart_item.cart.user == request.user:
        cart_item.delete()
        messages.success(request, 'Item removed from cart successfully.')
        return redirect('cart_detail')

    messages.error(request, 'You do not have permission to remove items from the cart.')
    return redirect('cart_detail')


@login_required
def cart_detail(request):
    cart_items = []
    total_amount = 0

    if request.user.groups.filter(name__in=['Seller', 'Admin']).exists():
        # Fetch all cart items if user is an admin or seller
        cart_items = CartItem.objects.select_related('product').all()
    elif request.user.groups.filter(name='Buyer').exists():
        # If the user is a buyer, show their specific cart items
        try:
            cart = Cart.objects.get(user=request.user)  # Get the buyer's cart
            cart_items = CartItem.objects.filter(cart=cart).select_related('product')
        except Cart.DoesNotExist:
            cart_items = []
            messages.info(request, 'Your cart is empty.')

    # Calculate total amount for the displayed cart items
    total_amount = sum(item.quantity * item.product.price for item in cart_items)

    return render(request, 'cart/cart.html', {'cart_items': cart_items, 'total_amount': total_amount})