from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),  # Page d'accueil
    path('menu/', views.MenuView.as_view(), name="menu"),  # Page du menu
    path('reservation/', views.ReservationClientView.as_view(), name="reservation-client"),  # Formulaire client
    path('reservations/', views.ReservationListView.as_view(), name="reservations"),  # Liste des réservations (admin)
]