    
from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),  # Page d'accueil
    path('menu/', views.MenuView.as_view(), name="menu"),  # Page du menu
    path('reservation/', views.reservation_client_view, name="reservation-client"),  # Formulaire client
    path('reservation-express/', views.reservation_express_view, name="reservation-express"),  # Réservation express
    path('about/', views.AboutView.as_view(), name="about"),  # Page "À propos"
    path('mes-reservations/', views.MesreservationsView, name="mes-reservations"),  # Page "Mes réservations"
    path('reservation/modifier/<int:reservation_id>/', views.modifier_reservation_view, name="modifier-reservation"),
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('profil/', views.profil_view, name="profil"),
    path('profil/modifier/', views.update_profile_view, name="update_profile"),
]