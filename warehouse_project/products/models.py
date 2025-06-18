from django.db import models
from django.core.exceptions import ValidationError
from slugify import slugify


class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name='Название товара')
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    zone = models.IntegerField(verbose_name='Номер зоны')  # номер зоны

    def clean(self):
        if not self.name:
            raise ValidationError({'name': 'Название товара не может быть пустым'})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            # Handle duplicate slugs
            if Product.objects.filter(slug=self.slug).exists():
                counter = 1
                while Product.objects.filter(slug=f"{self.slug}-{counter}").exists():
                    counter += 1
                self.slug = f"{self.slug}-{counter}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
