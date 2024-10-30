from django.contrib import admin
from .models import Palet


@admin.register(Palet)
class PaletAdmin(admin.ModelAdmin):
    list_display = ("number", "description", "count", "pallets_from_the_date", "pallet_pick_up_date", "receipt_mark")
    list_filter = ("pallets_from_the_date", "pallet_pick_up_date", "receipt_mark")
