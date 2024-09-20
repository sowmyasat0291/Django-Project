from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm, ProductForm
from .models import Product
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator

def index_view(request):
    """Redirect to signup or login based on user authentication."""
    if request.user.is_authenticated:
        return redirect('product_list')  # Redirect to product list if logged in
    return redirect('login')  # Otherwise, redirect to login

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

@login_required
def product_list(request):
    # Optional: Add search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        products = Product.objects.filter(name__icontains=search_query)
    else:
        products = Product.objects.all()
    
    # Optional: Add pagination
    paginator = Paginator(products, 10)  # Show 10 products per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'products/product_list.html', {'page_obj': page_obj})

@login_required
def cart_view(request):
    # Implement your cart logic here
    return render(request, 'products/cart.html')  # Replace with your cart template

def logout_view(request):
    logout(request)  # Log the user out
    return redirect('login')  # Redirect to login after logout
