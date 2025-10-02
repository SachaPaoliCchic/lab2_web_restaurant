from modeltranslation.translator import register, TranslationOptions
from .models import Table, Reservation, Client

@register(Table)
class TableTranslationOptions(TranslationOptions):
    fields = ('numero',)

@register(Reservation)
class ReservationTranslationOptions(TranslationOptions):
    fields = ('nombre_personnes',)

@register(Client)
class ClientTranslationOptions(TranslationOptions):
    fields = ('nom',)