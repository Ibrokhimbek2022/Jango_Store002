from django.urls import path
from . import views

# http://127.0.01:8000/cart/checkout
urlpatterns = [
    path("", views.cart_view, name="cart"),
    path("checkout/", views.checkout_view, name="checkout"),
]








