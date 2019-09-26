from bootstrap_datepicker_plus import DatePickerInput
from django.views.generic.edit import CreateView
from .models import Letter
from .forms import LetterForm

class LetterCreateView(CreateView):
    model = Letter
    # fields = ['nom', 'email', 'numerofact', 'date_debut', 'date_fin']
    form_class = LetterForm
    
    
    
    def get_form(self):
        form = super().get_form()
        form.fields['date_debut'].widget = DatePickerInput().start_of('letter date')
        form.fields['date_fin'].widget = DatePickerInput().end_of('letter date')
        return form
      