# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ProductForm
from .models import Product

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
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

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})
