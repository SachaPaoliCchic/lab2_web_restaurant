from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name="index"),  # Page d'accueil
    path('menu/', views.MenuView.as_view(), name="menu"),  # Page du menu
    path('reservation/', views.reservation_client_view, name="reservation-client"),  # Formulaire client
    path('reservation-express/', views.reservation_express_view, name="reservation-express"),  # Réservation express
    path('about/', views.AboutView.as_view(), name="about"),  # Page "À propos"
    path('signup/', views.signup_view, name="signup"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
]