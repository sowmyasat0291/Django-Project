#Product/views.py
import jwt
from datetime import datetime, timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User, Group
from django.conf import settings
from django.core.paginator import Paginator
from django.contrib import messages
from .forms import SignUpForm, ProductForm
from Cart.models import Cart, CartItem
from .models import Product

# Redirect to signup or login based on user authentication
def index_view(request):
    if request.user.is_authenticated:  # Check if user is authenticated using JWT middleware
        return redirect('product_list')
    return render(request, 'products/welcome.html')

def create_groups():
    groups = ['Admin', 'Seller', 'Buyer']
    for group in groups:
        Group.objects.get_or_create(name=group)

# Signup view
def signup_view(request):
    create_groups()  # Create groups if they don't exist
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')  # Get the selected role
            if role:
                group = Group.objects.get(name=role)  # Assuming you've created groups for roles
                group.user_set.add(user)  # Assign user to the selected group
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
                login(request, user)
                # Create JWT token with roles
                payload = {
                    'user_id': user.id,
                    'role': user.groups.first().name if user.groups.exists() else 'User',  # Get user role
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
    if not request.user.is_authenticated:  # Check if user is authenticated
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
    if request.user.is_authenticated and request.role in ['Admin', 'Seller']:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product created successfully.')
                return redirect('product_list')
        else:
            form = ProductForm()
        return render(request, 'products/product_form.html', {'form': form, 'action': 'Create'})
    messages.error(request, 'You do not have permission to create a product.')
    return redirect('product_list')


# Update a product
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.user.is_authenticated and request.role in ['Admin', 'Seller']:
        if request.method == 'POST':
            form = ProductForm(request.POST, request.FILES, instance=product)
            if form.is_valid():
                form.save()
                messages.success(request, 'Product updated successfully.')
                return redirect('product_list')
        else:
            form = ProductForm(instance=product)
        return render(request, 'products/product_form.html', {'form': form, 'action': 'Update'})
    messages.error(request, 'You do not have permission to update this product.')
    return redirect('product_list')


# Delete a product
def delete_product(request, pk):
    # Only admins can delete products
    if request.user.is_authenticated and request.user.groups.filter(name='Admin').exists():
        product = get_object_or_404(Product, pk=pk)
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Product deleted successfully.')
            return redirect('product_list')

        return render(request, 'products/product_confirm_delete.html', {'product': product})
    
    messages.error(request, 'You do not have permission to delete this product.')
    return redirect('product_list')

# View Cart

def cart_view(request):
    # Restrict Sellers from viewing the cart
    if request.user.groups.filter(name='Seller').exists():
        messages.error(request, 'Sellers are not allowed to view the cart.')
        return redirect('product_list')
    
    # Get or create a cart for the user
    cart, _ = Cart.objects.get_or_create(user=request.user)
    
    # Get all cart items for the user's cart
    cart_items = CartItem.objects.filter(cart=cart)

    # Calculate total amount using a generator expression
    total_amount = 0
    for item in cart_items:
        item.total_price = item.quantity * item.product.price
        total_amount += item.total_price
        
    # Handle the increase/decrease quantity action
    if request.method == 'POST':
        item_id = request.POST.get('item_id')
        action = request.POST.get('action')
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)

        if action == 'increase':
            cart_item.quantity += 1
        elif action == 'decrease' and cart_item.quantity > 1:
            cart_item.quantity -= 1
        
        cart_item.save()
        return redirect('cart_view')

    # Prepare the context for the template
    context = {
        'items': cart_items,  # Pass cart items to the template
        'total_amount': total_amount,
    }
    
    # Render the cart template
    return render(request, 'cart/cart.html', context)

# Logout view
def logout_view(request):
    response = redirect('login')
    response.delete_cookie('jwt')  # Remove JWT token cookie
    return response
