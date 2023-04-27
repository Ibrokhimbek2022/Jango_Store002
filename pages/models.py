from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.


class Category(models.Model):
    title = models.CharField(verbose_name="Название категории", max_length=150, unique=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Subcategory(models.Model):
    title = models.CharField(verbose_name="Название подкатегории", max_length=150, unique=True)
    slug = models.SlugField(default="", null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория", null=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)


    class Meta:
        verbose_name = "Подкатегория"
        verbose_name_plural = "Подкатегории"


class Product(models.Model):
    PRODUCT_TYPES = (
        ("new", "New"),
        ("sale", "Sale"),
        ("sold", "Sold"),
    )
    title = models.CharField(verbose_name="Название продукта", max_length=150, unique=True)
    slug = models.SlugField(default="", null=True, blank=True)
    description = models.TextField(verbose_name="Описание")
    price = models.IntegerField(verbose_name="Цена", default=0)
    quantity = models.IntegerField(verbose_name="Кол-во продукта", default=0)
    views = models.IntegerField(verbose_name="Кол-во просмотров", default=0)
    product_type = models.CharField(
        max_length=10,
        choices=PRODUCT_TYPES,
        blank=True,
        null=True,
        default=""
    )
    subcategory = models.ForeignKey(Subcategory, on_delete=models.SET_NULL, verbose_name="Подкатегория", null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, verbose_name="Категория", null=True)

    def get_class_by_type(self):
        TYPES_CLASSES = {
            "new": "info",
            "sale": "primary",
            "sold": "danger"
        }
        if self.product_type:
            return TYPES_CLASSES[self.product_type]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    photo = models.ImageField(verbose_name="Фото", upload_to="products/", null=True, blank=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name="Продукт")

# CategoryModel
    # title
# SubCategoryModel
    # title
    # category_id
# Product
    # title
    # description
    # price
    # quantity
    # views
    # product_type (new, sale, sold)
    # category
# ProductImage
    # photo
    # product_id
