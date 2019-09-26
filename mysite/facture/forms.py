from bootstrap_datepicker_plus import DatePickerInput
from django import forms
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
            'date_debut': DatePickerInput(format='%Y-%d-%m').start_of('date facture'),
            'date_echeance' : DatePickerInput(format='%Y-%d-%m').end_of('date facture'),
            'date_prestation' : DatePickerInput(format='%Y-%d-%m')
        }

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields ='__all__'





