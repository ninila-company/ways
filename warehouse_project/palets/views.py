import os
import time

import requests
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from dotenv import load_dotenv
from django.db.models import Q

from .models import Palet

# Загружаем переменные окружения
load_dotenv()


def palet_list(request):
    search_query = request.GET.get('search', '').strip()
    palets = Palet.objects.filter(receipt_mark=False)
    if search_query:
        words = search_query.split()
        q = Q()
        for word in words:
            q &= Q(products_quantity__product__product_name__icontains=word)
        palets = palets.filter(q)
    palets = palets.order_by("number").distinct()
    return render(request, "palets/palet_list.html", {"palets": palets, "search": search_query})


def send_palet(request, palet_id):
    if request.method == "POST":
        try:
            palet = get_object_or_404(Palet, id=palet_id)

            # Получаем список продуктов в паллете с количеством
            products_list = []
            for product_quantity in palet.products_quantity.all():
                products_list.append(
                    f"{product_quantity.product.product_name} - {product_quantity.quantity} шт."
                )
            products_text = "\n".join(products_list)

            payload = {
                "text": f"Паллета № {palet.number}",
                "textHtml": f"<p>Паллета {palet.number}\nСодержимое:\n{products_text}</p>",
                "label": f"Паллета № {palet.number} {time.strftime('%d.%m.%Y %H:%M')}",
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('YOUGILE_API_KEY')}",
            }

            url = f"https://ru.yougile.com/api-v2/chats/{os.getenv('YOUGILE_CHAT_ID')}/messages"

            response = requests.request("POST", url, json=payload, headers=headers)

            try:
                response.raise_for_status()
                messages.success(request, f"Паллета №{palet.number} успешно заказана!")
                # Помечаем паллету как полученную после успешной отправки
                palet.receipt_mark = True
                palet.save()
            except requests.exceptions.HTTPError as e:
                messages.error(
                    request, f"Ошибка при заказе паллеты №{palet.number}: {str(e)}"
                )

            return HttpResponseRedirect(reverse("palets:palet_list"))

        except Exception as e:
            messages.error(request, f"Произошла ошибка: {str(e)}")
            return HttpResponseRedirect(reverse("palets:palet_list"))
