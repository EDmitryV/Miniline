from django.urls import path
from . import views

urlpatterns = [
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('', views.index, name="index"),
    path('products/', views.products, name="products"),
    path('single-product/', views.single_product, name="single-product"),
    path('cart/', views.cart, name="cart"),
]
