from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.conf import settings
# from .models import Image
from .models import Prestataire, Facture, Client


class PrestataireForm(forms.ModelForm):
    class Meta:
        model = Prestataire
        fields = '__all__'


class FactureForm(forms.ModelForm):
    class Meta:
        model = Facture
        fields ='__all__'
        widgets = {
            'date_debut': DatePickerInput().start_of('date facture'),
            'date_echeance' : DatePickerInput().end_of('date facture'),
            'date_prestation' : DatePickerInput()
        }



class FactureSearchForm(forms.Form):
    # Recherche de factures
    
    search_text_client = forms.CharField(
        required = False,
        label = 'Nom client',
        widget = forms.TextInput(attrs = {'palceholder': 'Nom ou partie du nom'})
    )

    search_text_prestataire = forms.CharField(
        required = False,
        label = 'Nom prestataire',
        widget = forms.TextInput(attrs = {'palceholder': 'Nom ou partie du nom'})
    )

    search_date_facture_gt = forms.DateField(
        required = False,
        label = 'Facture: Date de début inclue',
        widget = DatePickerInput(format='%Y-%m-%d')
        )            

    search_date_facture_lt = forms.DateField(
        required = False,
        label = 'Facture: Date de fin inclue',
        widget = DatePickerInput(format='%Y-%m-%d')
        )            


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields ='__all__'





