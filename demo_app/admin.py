from django.contrib import admin
from .models import Client, Table, Reservation
from django.utils.html import format_html

class ClientAdmin(admin.ModelAdmin):
    list_display = ('nom', 'email', 'image_thumbnail')
    search_fields = ('nom', 'email')
    ordering = ('nom',)
    readonly_fields = ('image_preview',)

    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:40px; border-radius:5px;" />', obj.image.url)
        return "-"
    image_thumbnail.short_description = "Photo"

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height:150px; border-radius:10px;" />', obj.image.url)
        return "Aucune image"
    image_preview.short_description = "Aperçu"

    fieldsets = (
        (None, {
            'fields': ('nom', 'email', 'image', 'image_preview')
        }),
    )

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