from django.shortcuts import render, HttpResponse
from .models import Product, Category, Subcategory
# Create your views here.


def home_view(request):
    return render(request, "pages/index.html")


def shop_view(request):
    products = Product.objects.all()
    context = {
        "products": products
    }
    return render(request, "pages/shop.html", context)