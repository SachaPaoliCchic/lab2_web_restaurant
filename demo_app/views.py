from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Client, Table, Reservation
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class MenuView(TemplateView):
    template_name = "menu.html"

class AboutView(TemplateView):
    template_name = "about.html"

def reservation_client_view(request):
    if request.method == 'POST':
        # Récupérer les données du formulaire
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        nombre_personnes = int(request.POST.get('nombre_personnes'))
        date_str = request.POST.get('date')
        
        # Convertir la date
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        # Créer ou récupérer le client
        client, created = Client.objects.get_or_create(
            email=email,
            defaults={'nom': nom}
        )
        
        # Trouver une table disponible avec la capacité suffisante
        table_disponible = Table.objects.filter(
            capacite__gte=nombre_personnes
        ).exclude(
            reservation__date=date
        ).first()
        
        if table_disponible:
            reservation = Reservation.objects.create(
                client=client,
                table=table_disponible,
                date=date,
                nombre_personnes=nombre_personnes
            )
            messages.success(request, f'Réservation confirmée pour {nom} le {date} à la table {table_disponible.numero}!')
            return redirect('reservation-client')
        else:
            messages.error(request, 'Aucune table disponible pour cette date et ce nombre de personnes.')
    
    return render(request, 'reservation_client.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            messages.success(request, "Inscription réussie ! Connectez-vous.")
            return redirect('login')
    return render(request, 'register.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = User.objects.get(email=email)
            user_auth = authenticate(request, username=user.username, password=password)
            if user_auth is not None:
                login(request, user_auth)
                messages.success(request, f"Bienvenue {user_auth.username} !")
                return redirect('index')
            else:
                messages.error(request, "Mot de passe incorrect.")
        except User.DoesNotExist:
            messages.error(request, "Aucun utilisateur avec cet email.")
    return render(request, 'connection.html')

def logout_view(request):
    logout(request)
    return redirect('index')


