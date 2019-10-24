from bootstrap_datepicker_plus import DatePickerInput
from django import forms
from django.forms import formset_factory, inlineformset_factory
from django.conf import settings
# from .models import Image
from .models import Prestataire, Facture, Client, PrestToFact


class PrestataireForm(forms.ModelForm):
    class Meta:
        model = Prestataire
        fields = '__all__'

 
class FactureForm(forms.ModelForm):
    
    def __init__(self, *args, **kwargs):
        super(FactureForm, self).__init__(*args, **kwargs)
        
    
    class Meta:
    
        model = Facture
        fields ='__all__'
        widgets = {
            'date_debut': DatePickerInput().start_of('date facture'),
            'date_echeance' : DatePickerInput().end_of('date facture'),
            'date_prestation' : DatePickerInput()
        }

    def get_form(self):
        form = super().get_form()
        form.fields['date_debut'].widget = DatePickerInput().start_of('facture date')
        form.fields['date_echeance'].widget = DatePickerInput().end_of('facture date')
        form.fields['date_prestation'].widget = DatePickerInput().end_of('facture date')
        return form
    
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




class PrestToFactForm(forms.ModelForm):

    class Meta:
        model = PrestToFact
        exclude = ()
       

''' PrestToFactFormset = inlineformset_factory(
    Facture, PrestToFact, form=PrestToFactForm,
    fields =['quantite', 'prix_unitaire_HT'],
    )
 '''
