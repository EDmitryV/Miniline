from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def about(request):
    context = {}
    return render(request, 'store/about.html', context)


def contact(request):
    context = {}
    return render(request, 'store/contact.html', context)


def index(request):
    context = {}
    return render(request, 'store/index.html', context)


def products(request):
    context = {}
    return render(request, 'store/products.html', context)


def single_product(request):
    context = {}
    return render(request, 'store/single-product.html', context)


def cart(request):
    context = {}
    return render(request, 'store/cart.html', context)
