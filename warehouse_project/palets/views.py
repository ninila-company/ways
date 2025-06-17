from django.shortcuts import render, get_object_or_404
from .models import Palet
import requests
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import messages
import time
import os
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

def palet_list(request):
    palets = Palet.objects.filter(receipt_mark=False).order_by('number')
    return render(request, 'palets/palet_list.html', {'palets': palets})


def send_palet(request, palet_id):
    if request.method == 'POST':
        try:
            palet = get_object_or_404(Palet, id=palet_id)
            
            # Получаем список продуктов в паллете
            products_list = [product.product_name for product in palet.description.all()]
            products_text = "\n".join(products_list)

            payload = {
                "text": f"Паллета № {palet.number}",
                "textHtml": f"<p>Паллета {palet.number}\nСодержимое:\n{products_text}</p>",
                "label": f"Паллета № {palet.number} {time.strftime('%d.%m.%Y %H:%M')}"
            }

            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Bearer {os.getenv('YOUGILE_API_KEY')}"
            }

            url = f"https://ru.yougile.com/api-v2/chats/{os.getenv('YOUGILE_CHAT_ID')}/messages"

            response = requests.request("POST", url, json=payload, headers=headers)
            
            try:
                response.raise_for_status()
                messages.success(request, f'Паллета №{palet.number} успешно заказана!')
                # Помечаем паллету как полученную после успешной отправки
                palet.receipt_mark = True
                palet.save()
            except requests.exceptions.HTTPError as e:
                messages.error(request, f'Ошибка при заказе паллеты №{palet.number}: {str(e)}')
            
            return HttpResponseRedirect(reverse('palets:palet_list'))
            
        except Exception as e:
            messages.error(request, f'Произошла ошибка: {str(e)}')
            return HttpResponseRedirect(reverse('palets:palet_list'))
