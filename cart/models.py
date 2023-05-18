from django.db import models
from accounts.models import CustomUser
from pages.models import Product


# Create your models here.


class Order(models.Model):
    pass


class OrderProduct(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)

    @property
    def get_cart_total_price(self):
        order_products = self.orderproduct_set.all()
        return sum([item.get_total_price for item in order_products])

    @property
    def get_cart_total_quantity(self):
        order_products = self.orderproduct_set.all()
        return sum([item.quantity for item in order_products])


class OrderProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0)
    added_at = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.product.price * self.quantity


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=100)
    company_name = models.CharField(max_length=100, blank=True, null=True)


class ShippingAddress(models.Model):
    address_1 = models.CharField(max_length=100)
    address_2 = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)

