from django.shortcuts import render, HttpResponse
from .models import Product, Category, Subcategory
from django.core.paginator import Paginator
# Create your views here.


def home_view(request):
    return render(request, "pages/index.html")


def get_paginator(request, queryset):
    paginator = Paginator(queryset, 2)
    page = request.GET.get("page")
    result = paginator.get_page(page)
    return result

def shop_view(request):
    products = Product.objects.all()
    result = get_paginator(request, products)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)


def subcategory_articles_view(request, slug):
    subcategory = Subcategory.objects.get(slug=slug)
    products = Product.objects.filter(subcategory=subcategory)
    result = get_paginator(request, products)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)


def product_detail_view(request, slug):
    product = Product.objects.get(slug=slug)
    category = product.category
    related_products = Product.objects.filter(category=category).order_by("?")
    # related_products = [item for item in related_products if item.pk != product.pk]

    context = {
        "product_detail": product,
        "related_products": related_products[:4]
    }
    return render(request, "pages/product_detail.html", context)


