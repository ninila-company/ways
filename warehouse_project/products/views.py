from django.shortcuts import render
from .models import Product


def index(request):
    selected_product = None
    selected_zone = None
    products = Product.objects.all()

    # Получаем выбранный продукт из GET-запроса
    product_id = request.GET.get("product")
    if product_id:
        selected_product = Product.objects.get(zone=product_id)
        selected_zone = selected_product.zone

    return render(
        request,
        "products/index.html",
        {
            "products": products,
            "selected_product": selected_product,
            "selected_zone": selected_zone,
        },
    )


def zone_products(request, zone_id):
    # Получаем товары в выбранной зоне
    products_in_zone = Product.objects.filter(zone=zone_id)
    return render(
        request,
        "products/zone_products.html",
        {"products": products_in_zone, "zone_id": zone_id},
    )
