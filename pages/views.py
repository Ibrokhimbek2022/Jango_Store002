from django.shortcuts import render, HttpResponse, redirect
from .models import Product, Category, Subcategory
from django.core.paginator import Paginator
from .forms import ReviewForm
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
    import random

    product = Product.objects.get(slug=slug)
    category = product.category
    related_products = Product.objects.filter(category=category).order_by("?")
    # related_products = [item for item in related_products if item.pk != product.pk]

    if request.method == "POST":
        form = ReviewForm(data=request.POST)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = request.user
            form.product = product
            form.save()
            return redirect("product_detail", product.slug)
    else:
        form = ReviewForm()

    reviews = product.reviews.all()
    try:
        rating = sum([x.rating for x in reviews if x.rating]) / reviews.count()
    except:
        rating = 0
    context = {
        "product_detail": product,
        "related_products": related_products[:4],
        "form": form,
        "reviews": reviews,
        "rating": round(rating, 1)
    }
    return render(request, "pages/product_detail.html", context)


