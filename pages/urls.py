from django.urls import path
from . import views

urlpatterns = [
    path("", views.home_view, name="home"),
    path("categories/", views.shop_view, name="shop"),
    path("categories/<slug:slug>/", views.subcategory_articles_view, name="subcategory_articles"),
    path("products/<slug:slug>/", views.product_detail_view, name="product_detail")
]








