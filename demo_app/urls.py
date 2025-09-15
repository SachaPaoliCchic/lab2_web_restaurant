from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),  # Page d'accueil
    path('menu/', views.MenuView.as_view(), name="menu"),  # Page du menu
    path('reservation/', views.reservation_client_view, name="reservation-client"),  # Formulaire client
    path('about/', views.AboutView.as_view(), name="about"),  # Page "À propos"
]