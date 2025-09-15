from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Client, Table, Reservation
from datetime import datetime

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


