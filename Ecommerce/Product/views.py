#Product/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from .forms import SignUpForm, ProductForm
from Cart.models import Cart, CartItem  # Import the Cart and CartItem models
from .models import Product

# Redirect to signup or login based on user authentication
def index_view(request):
    if request.user.is_authenticated:
        return redirect('product_list')  # Redirect to product list if logged in
    return render(request, 'products/welcome.html')  # Render the welcome page if not logged in

# Signup view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Optionally send a welcome email
            send_mail(
                'Welcome to Our Platform',
                'Thank you for signing up!',
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )
            return redirect('login')  # Redirect to login after signup
    else:
        form = SignUpForm()
    return render(request, 'products/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('product_list')  # Redirect after login
            else:
                form.add_error(None, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})

# List and search products
@login_required
def product_list(request):
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query).order_by('name')
    else:
        products = Product.objects.all().order_by('name')
    
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'page_obj': page_obj})

# Create a new product
@login_required
def create_product(request):
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list after creation
    else:
        form = ProductForm()
    css_link = '<link rel="stylesheet" type="text/css" href="{% static "css/style.css" %}">'

    context = {'form': form, 'action': 'Create'}
    return render(request, 'products/product_form.html', context)
# Update an existing product
@login_required
def update_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('product_list')  # Redirect to product list after updating
    else:
        form = ProductForm(instance=product)
    css_link = '<link rel="stylesheet" type="text/css" href="{% static "css/style.css" %}">'

    return render(request, 'products/product_form.html', {'form': form, 'action': 'Update'})
@login_required
def delete_product(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'Product deleted successfully.')
        return redirect('product_list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})

# View Cart (Dummy for now, implement as per your logic)
@login_required
def cart_view(request):
    cart = Cart.objects.get_or_create(user=request.user)
    cart_items = CartItem.objects.filter(cart=cart)
    total_amount = sum(item.product.price * item.quantity for item in cart_items)
    
    context = {
        'cart_items': cart_items,
        'total_amount': total_amount,
    }
    return render(request, 'cart/cart.html')

# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to login after logout
