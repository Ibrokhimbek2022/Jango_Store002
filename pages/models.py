from django.db import models
from django.template.defaultfilters import slugify
from django.urls import reverse
from accounts.models import CustomUser

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

    def get_absolute_url(self):
        return reverse("subcategory_articles", kwargs={"slug": self.slug})



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

    def get_absolute_url(self):
        return reverse("product_detail", kwargs={"slug": self.slug})

    def get_first_photo(self):
        photo = self.productimage_set.all().first()
        if photo is not None:
            return photo.photo.url
        return "https://images.satu.kz/126101312_w640_h640_razdel-v-razrabotketovary.jpg"


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


class Review(models.Model):
    RATING_CHOICES = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
    )
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    rating = models.IntegerField(choices=RATING_CHOICES, blank=True, null=True)


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
