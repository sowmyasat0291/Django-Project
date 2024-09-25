from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from Product.models import Product
from Cart.models import Cart

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, product=product)
    
    if not created:
        cart_item.quantity += 1
    cart_item.save()  # Save whether it's created or updated
    
    return redirect('view_cart')

@login_required
def remove_from_cart(request, product_id):
    cart_item = get_object_or_404(Cart, user=request.user, product_id=product_id)
    cart_item.delete()
    
    return redirect('view_cart')

@login_required
def view_cart(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart/cart.html', context)
