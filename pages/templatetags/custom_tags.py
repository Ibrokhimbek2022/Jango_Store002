from django import template

from pages.models import Category

register = template.Library()


@register.simple_tag()
def get_categories_data():
    categories = Category.objects.all()
    data = {category: category.subcategory_set.all() for category in categories}
    return data
