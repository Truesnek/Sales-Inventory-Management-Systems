from django.shortcuts import render

from django.shortcuts import render
from .models import Products, Customer

def home(request):
    return render(request, 'core/home.html')

def product_list(request):
    products = Products.objects.all()
    return render(request, 'core/product_list.html', {'products': products})

def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'core/customer_list.html', {'customers': customers})