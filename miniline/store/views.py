from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect


@login_required
def about(request):
    context = {'user': request.user.attr_name}
    return render(request, 'store/about.html', context)


@login_required
def contact(request):
    context = {'user': request.user}
    return render(request, 'store/contact.html', context)


@login_required
def index(request):
    context = {'user': request.user}
    return render(request, 'store/index.html', context)


@login_required
def products(request):
    context = {'user': request.user}
    return render(request, 'store/products.html', context)


@login_required
def single_product(request):
    context = {'user': request.user}
    return render(request, 'store/single-product.html', context)


@login_required
def cart(request):
    context = {'user': request.user}
    return render(request, 'store/cart.html', context)
