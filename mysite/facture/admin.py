from django.contrib import admin
from .models import Prestataire
from .models import Client
from .models import Facture


# Register your models here.
admin.site.register(Prestataire)
admin.site.register(Client)
admin.site.register(Facture)



