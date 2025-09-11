from django.contrib import admin
from .models import Client, Table, Reservation

admin.site.register(Client)
admin.site.register(Table)
admin.site.register(Reservation)