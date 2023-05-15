from accounts.models import CustomUser

from store import settings
from pages.models import Product
from .models import Order, OrderProduct


class CartFormAuthenticatedUser:
    pass


class CartForAnonymousUser:
    pass


def get_cart_data(request):
    pass


