from django.contrib import admin
from .models import Product, Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "price", "created_at")
    search_fields = ("name",)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "product", "user", "rating", "created_at")
    search_fields = ("product__name", "user__username")
