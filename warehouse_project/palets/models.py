from django.db import models
from django.utils.html import format_html


class Poducts_in_palet(models.Model):
    product_name = models.CharField(max_length=255, verbose_name='Товар')

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Продукт в палете"
        verbose_name_plural = "Продукты в палете"


class Palet(models.Model):
    number = models.IntegerField(verbose_name='Номер палеты')
    description = models.ManyToManyField(Poducts_in_palet, verbose_name='Описание палеты')
    pallets_from_the_date = models.DateField(verbose_name='Дата поступления')
    pallet_pick_up_date = models.DateField(blank=True, null=True, verbose_name='Дата вывоза')
    receipt_mark = models.BooleanField(default=False, verbose_name='Отметка о получении')

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name = "Палета"
        verbose_name_plural = "Палеты"

    def get_products_list(self):
        products = [product.product_name for product in self.description.all()]
        return format_html("<br>".join(products))
    get_products_list.short_description = "Продукты"
