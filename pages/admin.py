from django.contrib import admin
from .models import Category, Subcategory, Product, ProductImage


# Register your models here.


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "title")
    list_display_links = ("pk", "title")


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "category")
    list_display_links = ("pk", "title")
    prepopulated_fields = {"slug": ("title",)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "price", "views", "quantity", "category")
    list_display_links = ("pk", "title")
    readonly_fields = ("views",)
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ("category",)
    inlines = [
        ProductImageInline
    ]
