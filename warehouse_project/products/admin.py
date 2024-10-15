from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "zone", "count")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
