# views.py
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm, ProductForm
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views import View
from .models import Product
from django.shortcuts import get_object_or_404
import json


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

class ProductListCreateView(View):
    def get(self, request):
        products = Product.objects.all()
        data = list(products.values('id', 'name', 'price', 'description'))
        return JsonResponse(data, safe=False)

    @csrf_exempt
    def post(self, request):
        data = json.loads(request.body)
        form = ProductForm(data)
        if form.is_valid():
            product = form.save()
            return JsonResponse({'id': product.id, 'name': product.name, 'price': product.price, 'description': product.description}, status=201)
        return JsonResponse({'errors': form.errors}, status=400)

class ProductDetailView(View):
    def get(self, request, pk, *args, **kwargs):
        product = get_object_or_404(Product, pk=pk)
        data = {
            'name': product.name,
            'price': str(product.price),
            'description': product.description
        }
        return JsonResponse(data)