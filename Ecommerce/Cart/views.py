#Cart/views.py
import stripe
from django.conf import settings
from django.urls import reverse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Cart, CartItem
from Product.models import Product

# Stripe configuration
stripe.api_key = settings.STRIPE_SECRET_KEY

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

def checkout_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Prevent Admin from accessing the checkout process
    if request.user.groups.filter(name='Admin').exists():
        messages.error(request, 'Admins are not allowed to perform a checkout.')
        return redirect('product_list')

    # Fetch the user's cart items
    cart_items = CartItem.objects.filter(cart__user=request.user)

    # Calculate total amount for the session
    total_amount = sum(item.quantity * item.product.price for item in cart_items) * 100 
     # amount in paisa (INR)

    if total_amount <= 0:
        messages.error(request, 'Your cart is empty, add items before proceeding to checkout.')
        return redirect('cart_detail')

    # Create a Stripe Checkout Session
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],  # Allow credit card payments
        line_items=[{
            'price_data': {
                'currency': 'inr',
                'product_data': {
                    'name': 'Cart Purchase',
                },
                'unit_amount': total_amount,  # Total amount for all items
            },
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('checkout_success')),
        cancel_url=request.build_absolute_uri(reverse('checkout_cancel')),
    )

    # Redirect the user to Stripe's hosted checkout page
    return redirect(session.url, code=303)
# Success page
@login_required
def checkout_success(request):
    try:
        # Fetch the user's cart
        cart = Cart.objects.get(user=request.user)
        cart_items = CartItem.objects.filter(cart=cart)

        # Clear the cart items after successful payment
        cart_items.delete()

        # Optionally, you can delete the cart itself if needed
        # cart.delete()

        # Add success message
        messages.success(request, 'Payment completed successfully! Your cart has been cleared.')
    except Cart.DoesNotExist:
        messages.error(request, 'No cart found for this user.')

    # Render the checkout success template
    return render(request, 'cart/checkout_success.html')

# Cancel page
def checkout_cancel(request):
    messages.error(request, 'Payment was cancelled.')
    return render(request, 'cart/checkout_cancel.html')