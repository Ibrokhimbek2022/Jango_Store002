from django import template

from pages.models import Category, Review



register = template.Library()


@register.simple_tag()
def get_range_by_rating(rating):
    """"""
    res = []
    if not rating:
        return 0
    for i in range(1, 6):
        if rating >= i:
            res.append(1)
        elif rating < i:
            if rating % 1:
                if 0.5 not in res:
                    res.append(0.5)
                else:
                    res.append(0)
            else:
                res.append(0)
    return res


    # rating_range = [i for i in range(1, int(review.rating) + 1)]
    # return rating_range



@register.simple_tag()
def get_categories_data():
    categories = Category.objects.all()
    data = {category: category.subcategory_set.all() for category in categories}
    return data
