from django.contrib import admin
from django.http import HttpResponse
from django.template.loader import render_to_string
from weasyprint import HTML

from .models import Palet, Poducts_in_palet


@admin.register(Palet)
class PaletAdmin(admin.ModelAdmin):
    list_display = ("number", "pallets_from_the_date", "pallet_pick_up_date", "receipt_mark", "get_products_list")
    list_filter = ("pallets_from_the_date", "pallet_pick_up_date", "receipt_mark")
    filter_horizontal = ("description",)
    search_fields = ("description__product_name", "number")
    actions = ["print_selected_palets"]

    def get_products_list(self, obj):
        products = [product.product_name for product in obj.description.all()]
        return "<br>".join(products)

    get_products_list.short_description = "Продукты"
    get_products_list.allow_tags = True

    def print_selected_palets(self, request, queryset):
        # Получаем все выбранные палеты
        try:
            palets = queryset
            html_string = render_to_string('palets/print_selected_palets.html', {'palets': palets})
            pdf_file = HTML(string=html_string).write_pdf()

            response = HttpResponse(pdf_file, content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="selected_palets.pdf"'
            return response
        except Exception as e:
            self.message_user(request, f"Ошибка при генерации PDF: {str(e)}", level='error')
            return

    print_selected_palets.short_description = "Печать выбранных палет"


@admin.register(Poducts_in_palet)
class Poducts_in_paletAdmin(admin.ModelAdmin):
    list_display = ("product_name",)
