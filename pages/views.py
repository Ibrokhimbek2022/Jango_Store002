from django.shortcuts import render, HttpResponse
from .models import Product, Category, Subcategory
from django.core.paginator import Paginator
# Create your views here.


def home_view(request):
    return render(request, "pages/index.html")




def shop_view(request):
    products = Product.objects.all()
    paginator = Paginator(products, 2)
    page = request.GET.get("page")
    result = paginator.get_page(page)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)


def subcategory_articles_view(request, slug):
    subcategory = Subcategory.objects.get(slug=slug)
    products = Product.objects.filter(subcategory=subcategory)
    paginator = Paginator(products, 2)
    page = request.GET.get("page")
    result = paginator.get_page(page)
    context = {
        "products": result
    }
    return render(request, "pages/shop.html", context)

def product_detail_view(request, slug):
    return render(request, "pages/product_detail.html")


