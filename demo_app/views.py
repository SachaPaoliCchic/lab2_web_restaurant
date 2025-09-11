from django.shortcuts import render

# Create your views here.
from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = "index.html"

class MenuView(TemplateView):
    template_name = "menu.html"

class ReservationClientView(TemplateView):
    template_name = "reservation_client.html"

class ReservationListView(TemplateView):
    template_name = "reservations.html"
