# from django.contrib import admin
# from .models import Prestataire
# from .models import Client
# from .models import Facture
# from .models import Prestation
# from .models import PrestToFact


# # Register your models here.
# admin.site.register(Prestataire)
# admin.site.register(Client)
# admin.site.register(Facture)
# admin.site.register(Prestation)
# admin.site.register(PrestToFact)
from django.contrib import admin
from . models import Prestataire, Client, Facture, Prestation, PrestToFact

# Register your models here.
admin.site.register(Prestataire)
admin.site.register(Client)

admin.site.register(Prestation)


class PrestToFactInline(admin.TabularInline):
    model = PrestToFact
    raw_id_fields = ['prest']

class PrestToFactAdmin(admin.ModelAdmin):
    list_display = ['id', 'prest', PrestToFact.prix_HT]

admin.site.register(PrestToFact, PrestToFactAdmin)


class FactureAdmin(admin.ModelAdmin):
    list_display = ['id', 'client', 'prestataire', 'ref_fact', 'type_facture', 'nombre_echeance']
    inlines = [PrestToFactInline]

admin.site.register(Facture, FactureAdmin)


