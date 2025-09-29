from django.contrib import admin
from .models import Client, Table, Reservation

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email')
    search_fields = ('nom', 'email')
    ordering = ('nom',)
    readonly_fields = ('email',)

class TableAdmin(admin.ModelAdmin):
    list_display = ('numero', 'capacite')
    search_fields = ('numero',)
    ordering = ('numero',)

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('client', 'table', 'date', 'nombre_personnes')
    search_fields = ('client__nom', 'table__numero')
    list_filter = ('date', 'table')
    ordering = ('-date',)
    exclude = ('nombre_personnes',)  

admin.site.register(Client, ClientAdmin)
admin.site.register(Table, TableAdmin)
admin.site.register(Reservation, ReservationAdmin)