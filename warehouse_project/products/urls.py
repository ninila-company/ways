from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("zone/<int:zone_id>/", views.zone_products, name="zone_products"),
]
