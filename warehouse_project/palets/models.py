from django.db import models
from django.utils.html import format_html


class Poducts_in_palet(models.Model):
    product_name = models.CharField(max_length=255)

    def __str__(self):
        return self.product_name


class Palet(models.Model):
    number = models.IntegerField(verbose_name='Номер палеты')
    description = models.ManyToManyField(Poducts_in_palet)
    pallets_from_the_date = models.DateField()
    pallet_pick_up_date = models.DateField(blank=True, null=True)
    receipt_mark = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)

    def get_products_list(self):
        products = [product.product_name for product in self.description.all()]
        return format_html("<br>".join(products))
    get_products_list.short_description = "Продукты"
