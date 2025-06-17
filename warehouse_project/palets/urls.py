from django.urls import path
from . import views

app_name = 'palets'

urlpatterns = [
    path('', views.palet_list, name='palet_list'),
    path('send/<int:palet_id>/', views.send_palet, name='send_palet'),
] 