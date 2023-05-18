from accounts.models import CustomUser

from store import settings
from pages.models import Product
from .models import Order, OrderProduct


class CartFormAuthenticatedUser:
    def __init__(self, request, product_id=None, actions=None):
        self.user = request.user

        if product_id and actions:
            self.add_or_delete(product_id, actions)

    def get_cart_info(self):
        user, created = CustomUser.objects.get_or_create(
            username=self.user.username,
            email=self.user.email
        )

        order, created = Order.objects.get_or_create(
            user=user
        )

        order_products = order.orderproduct_set.all()
        cart_total_quantity = order.get_cart_total_quantity
        cart_total_price = order.get_cart_total_price

        return {
            'cart_total_quantity': cart_total_quantity,
            'cart_total_price': cart_total_price,
            'order': order,
            'products': order_products
        }

    def add_or_delete(self, product_id, action):
        order = self.get_cart_info()["order"]
        product = Product.objects.get(pk=product_id)
        order_product, created = OrderProduct.objects.get_or_create(
            order=order,
            product=product
        )

        if action == "add" and product.quantity > 0:
            order_product.quantity += 1
            product.quantity -= 1
        else:
            order_product.quantity -= 1
            product.quantity += 1

        product.save()
        order_product.save()

        if order_product.quantity <= 0:
            order_product.delete()

    def clear(self):
        order = self.get_cart_info()["order"]
        items = order.orderproduct_set.all()

        for item in items:
            item.delete()
        order.save()


class CartFormUnauthenticatedUser:
    def __init__(self, request, product_id=None, actions=None):
        self.session = request.session
        self.cart = self.get_cart()

        if product_id and actions:
            self.key = str(product_id)
            self.product = Product.objects.get(pk=product_id)
            self.cart_product = self.cart.get(self.key)

            if actions == "add" and self.product_quantity > 0:
                self.add()
            elif actions == "delete":
                self.delete()

            self.product.save()
            self.save()

    def get_cart(self):
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session["cart"] = {}
        return cart

    def save(self):
        self.session.modified = True

    def get_cart_info(self):
        products = []
        order = {
            "get_cart_total_price": 0,
            "get_cart_total_quantity": 0
        }

        cart_total_quantity = order["get_cart_total_quantity"]
        cart_total_price = order["get_cart_total_price"]
        for key in self.cart:
            if self.cart[key]["quantity"] > 0:
                product_quantity = self.cart[key]["quantity"]
                cart_total_quantity += product_quantity
                product = Product.objects.get(pk=key)
                get_total_price = product.price * product_quantity

                cart_product = {
                    "pk": product.pk,
                    "product": {
                        "pk": product.title,
                        "title": product.title,
                        "price": product.price,
                        "get_first_photo": product.get_first_photo(),
                        "quantity": product.quantity,
                        "get_absolute_url": product.get_absolute_url()
                    },
                    "quantity": product_quantity,
                    "get_total_price": get_total_price
                }
                products.append(cart_product)
                order["get_cart_total_price"] += cart_product["get_total_price"]
                order["get_cart_total_quantity"] += cart_product["quantity"]
                cart_total_price = order["get_cart_total_price"]

        self.save()

        return {
            "cart_total_quantity": cart_total_quantity,
            "cart_total_price": cart_total_price,
            "order": order,
            "products": products
        }

    def add(self):
        if self.cart_product:
            self.cart_product["quantity"] += 1
        else:
            self.cart[self.key] = {
                "quantity": 1
            }

        self.product.quantity -= 1

    def delete(self):
        self.cart_product["quantity"] -= 1
        self.product.quantity += 1

        if self.cart_product["quantity"] <= 0:
            del self.cart[self.key]

    def clear(self):
        self.cart = {}


def get_cart_data(request):
    if request.user.is_authenticated:
        user_cart = CartFormUnauthenticatedUser(request)
        cart_info = user_cart.get_cart_info()
    else:
        session_cart = CartFormUnauthenticatedUser(request)
        cart_info = session_cart.get_cart_info()

    return {
        "cart_total_quantity": cart_info["cart_total_quantity"],
        "cart_total_price": cart_info["cart_total_price"],
        "order": cart_info["order"],
        "products": cart_info["products"]
    }
