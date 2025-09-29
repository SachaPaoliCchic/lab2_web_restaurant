from django.shortcuts import render, redirect
from django.contrib import messages
from django.views.generic import TemplateView
from .models import Client, Table, Reservation
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.paginator import Paginator

# Create your views here.

class IndexView(TemplateView):
    template_name = "index.html"

class MenuView(TemplateView):
    template_name = "menu.html"

class AboutView(TemplateView):
    template_name = "about.html"

def reservation_client_view(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            nom = request.user.username
            email = request.user.email
        else:
            nom = request.POST.get('nom')
            email = request.POST.get('email')
        nombre_personnes = int(request.POST.get('nombre_personnes'))
        date_str = request.POST.get('date')
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        client, created = Client.objects.get_or_create(
            email=email,
            defaults={'nom': nom}
        )
        table_disponible = Table.objects.filter(
            capacite__gte=nombre_personnes
        ).exclude(
            reservation__date=date
        ).first()
        if table_disponible:
            Reservation.objects.create(
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

def reservation_express_view(request):
    today = timezone.localdate()
    tables = Table.objects.exclude(reservation__date=today).order_by('capacite')
    if request.method == 'POST' and request.user.is_authenticated:
        table_id = request.POST.get('table_id')
        table = Table.objects.get(id=table_id)
        client, created = Client.objects.get_or_create(
            email=request.user.email,
            defaults={'nom': request.user.username}
        )
        Reservation.objects.create(
            client=client,
            table=table,
            date=today,
            nombre_personnes=table.capacite
        )
        messages.success(request, f"Réservation confirmée pour aujourd'hui à la table {table.numero}!")
        return redirect('reservation-express')
    return render(request, 'reservation_express.html', {'tables': tables})

def MesreservationsView(request):
    if not request.user.is_authenticated:
        return redirect('login')
    client = Client.objects.filter(email=request.user.email).first()
    if request.method == 'POST':
        delete_id = request.POST.get('delete_id')
        if delete_id:
            Reservation.objects.filter(id=delete_id, client=client).delete()
            messages.success(request, "Réservation supprimée.")
            return redirect('mes-reservations')
    reservations_list = Reservation.objects.filter(client=client).order_by('-date') if client else []
    paginator = Paginator(reservations_list, 5)  # 5 réservations par page
    page_number = request.GET.get('page')
    reservations = paginator.get_page(page_number)
    return render(request, 'mes_reservations.html', {'reservations': reservations})

def signup_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        image = request.FILES.get('image')
        if password1 != password2:
            messages.error(request, "Les mots de passe ne correspondent pas.")
        elif User.objects.filter(username=username).exists():
            messages.error(request, "Ce nom d'utilisateur existe déjà.")
        elif User.objects.filter(email=email).exists():
            messages.error(request, "Cet email est déjà utilisé.")
        else:
            user = User.objects.create_user(username=username, email=email, password=password1)
            Client.objects.create(nom=username, email=email, image=image)
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

def modifier_reservation_view(request, reservation_id):
    if not request.user.is_authenticated:
        return redirect('login')
    reservation = Reservation.objects.filter(id=reservation_id, client__email=request.user.email).first()
    if not reservation:
        messages.error(request, "Réservation introuvable ou non autorisée.")
        return redirect('mes-reservations')
    if request.method == 'POST':
        nombre_personnes = int(request.POST.get('nombre_personnes'))
        # Cherche une table dispo avec la bonne capacité pour la même date
        table_disponible = Table.objects.filter(
            capacite__gte=nombre_personnes
        ).exclude(
            reservation__date=reservation.date
        ).order_by('capacite').first()
        if table_disponible:
            reservation.nombre_personnes = nombre_personnes
            reservation.table = table_disponible
            reservation.save()
            messages.success(request, "Réservation modifiée avec succès !")
            return redirect('mes-reservations')
        else:
            messages.error(request, "Aucune table disponible pour cette date et ce nombre de personnes.")
    return render(request, 'update_reservation.html', {'reservation': reservation})


def profil_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    client = Client.objects.filter(email=request.user.email).first()
    return render(request, 'profil.html', {'client': client})

def update_profile_view(request):
    if not request.user.is_authenticated:
        return redirect('login')
    client = Client.objects.filter(email=request.user.email).first()
    if request.method == 'POST':
        nom = request.POST.get('nom')
        email = request.POST.get('email')
        image = request.FILES.get('image')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = request.user
        # Vérifie d'abord la cohérence des mots de passe
        if password1 or password2:
            if password1 != password2:
                messages.error(request, "Les mots de passe ne correspondent pas.")
                return render(request, 'update_profile.html', {'client': client})
        if client:
            client.nom = nom
            client.email = email
            if image:
                client.image = image
            client.save()
            # Mise à jour du mot de passe si renseigné et confirmé
            if password1 and password1 == password2:
                user.set_password(password1)
                user.save()
                messages.success(request, "Mot de passe modifié ! Veuillez vous reconnecter.")
                return redirect('login')
            messages.success(request, "Profil mis à jour !")
            return redirect('profil')
    return render(request, 'update_profile.html', {'client': client})