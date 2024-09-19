from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import SignUpForm
from .models import Product

# Sign Up view
def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('product_list')
    else:
        form = SignUpForm()
    return render(request, 'products/signup.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('product_list')
    else:
        form = AuthenticationForm()
    return render(request, 'products/login.html', {'form': form})

# Product list view (login required)
@login_required
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})
def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})

