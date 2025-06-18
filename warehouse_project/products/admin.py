from django.contrib import admin
from .models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "zone")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}
    list_filter = ("zone",)
