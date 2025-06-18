from django.db import models
from django.utils.text import slugify


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    zone = models.IntegerField(verbose_name='Номер зоны')  # номер зоны

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
