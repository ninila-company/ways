from django.db import models


class Palet(models.Model):
    number = models.IntegerField(verbose_name='Номер палеты')
    description = models.CharField(max_length=255)
    count = models.PositiveIntegerField(default=0)
    pallets_from_the_date = models.DateField()
    pallet_pick_up_date = models.DateField()
    receipt_mark = models.BooleanField(default=False)

    def __str__(self):
        return str(self.number)
