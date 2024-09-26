import jwt
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import SignUpForm, ProductForm
from Cart.models import Cart, CartItem
from .models import Product

# Redirect to signup or login based on user authentication
def index_view(request):
    if request.user is not None:  # Check if user is authenticated using JWT middleware
        return redirect('product_list')
    return render(request, 'products/welcome.html')

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = SignUpForm()
    return render(request, 'products/signup.html', {'form': form})

# Login view (JWT Authentication)
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Create JWT token
                payload = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(minutes=30),  # Token expires in 30 mins
                    'iat': datetime.utcnow()
                }
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')

                # Set the token in a HttpOnly cookie
                response = redirect('product_list')
                response.set_cookie('jwt', token, httponly=True)

                return response
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()

    return render(request, 'products/login.html', {'form': form})

# List and search products
def product_list(request):
    if request.user is None:  # Check if user is authenticated
        return redirect('login')

    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query).order_by('name')
    else:
        products = Product.objects.all().order_by('name')

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'page_obj': page_obj})

# Create a new product
def create_product(request):
    if request.user is None:  # Check if user is authenticated
        return redirect('login')

    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product created successfully.')
            return redirect('product_list')
    else:
        form = ProductForm()
    
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})

# Update an existing product
def update_product(request, pk):
    if request.user is None:  # Check if user is authenticated
        return redirect('login')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Product updated successfully.')
            return redirect('product_list')
    else:
        form = ProductForm(instance=product)
    
    return render(request, 'products/product_form.html', {'form': form, 'action': 'Update'})

# Delete a product
def delete_product(request, pk):
    if request.user is None:  # Check if user is authenticated
        return redirect('login')

    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# View Cart
def cart_view(request):
    if request.user is None:  # Check if user is authenticated
        return redirect('login')

    cart, _ = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)

    # Create a list to hold calculated totals for items
    for item in cart_items:
        item.total_price = item.product.price * item.quantity

    total_amount = sum(item.total_price for item in cart_items)

    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart/cart.html', context)

# Logout view
def logout_view(request):
    response = redirect('login')
    response.delete_cookie('jwt')  # Remove JWT token cookie
    return response
