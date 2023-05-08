from django import template

from pages.models import Category

register = template.Library()

@register.filter()
def rating_range(val=0):
    return range(val)


@register.simple_tag()
def get_categories_data():
    categories = Category.objects.all()
    data = {category: category.subcategory_set.all() for category in categories}
    return data
