from bootstrap_datepicker_plus import DatePickerInput
from . models import Letter
from django import forms

class LetterForm(forms.ModelForm):
    class Meta:
        model = Letter
        fields = ['nom', 'email', 'numerofact', 'date_debut', 'date_fin']
        widgets = {
            'date_debut': DatePickerInput().start_of('date letter'),
            'date_fin' : DatePickerInput().end_of('date letter')
        }