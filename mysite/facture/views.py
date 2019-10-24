#coding: utf-8
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.generic import View

from django.utils import timezone
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.template.loader import render_to_string

#from weasyprint import HTML
from django.conf import settings
# from easy_pdf.views import PDFTemplateView

# from xhtml2pdf import pisa
from django.template.loader import get_template
from django.template import Context

from .forms import PrestataireForm, ClientForm, FactureForm, PrestToFact
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic.detail import DetailView
from django.forms import modelformset_factory, inlineformset_factory

from bootstrap_datepicker_plus import DatePickerInput
import weasyprint
from io import BytesIO
from weasyprint import HTML, CSS

# Ajout pour recherche
# Nécessite installation django-search-views
from search_views.search import SearchListView
from search_views.filters import BaseFilter
from .forms import *
# fin ajout

from django.urls import reverse_lazy

from .models import *



@login_required (redirect_field_name='my_redirect_field')
def prestataire(request):
    return render(request=request,
                  template_name="prestataire_list.html",
                  context={"prestataires": Prestataire.objects.all})

@login_required
def client(request):
    return render(request=request,
                  template_name="client_list.html",
                  context={"clients": Client.objects.all})



class FactureFilters(BaseFilter):
    search_fields = {
        'search_text_client': ['client__nom_societe'],
        'search_text_prestataire': ['prestataire__nom'],
        'search_date_facture_gt': {'operator': '__gte', 'fields': ['date_debut']},
        'search_date_facture_lt': {'operator': '__lte', 'fields': ['date_debut']},
    }


class FactureSearchList(SearchListView):
    model = Facture
    template_name = "facture_list.html"
    form_class = FactureSearchForm
    filter_class = FactureFilters


def Facture_PDF(request, Facture_id):
   
    context = Facture.pourPDF(request, Facture_id)

    html = render_to_string('facture/facture_detail_PDF.html',
                            context)
    response = HttpResponse(content_type = 'application/PDF')
    response['Content-Disposition'] = 'filename="facture_{}.pdf"'.format(Facture_id)
    weasyprint.HTML(string=html).write_pdf(response)
    return response

def Facture_PDF2(request, Facture_id):
       
    context = Facture.pourPDF(request, Facture_id)

    html = render_to_string('facture/facture_PDF.html',
                            context)
    response = HttpResponse(content_type = 'application/PDF')
    response['Content-Disposition'] = 'filename="facture_{}.pdf"'.format(Facture_id)
    weasyprint.HTML(string=html).write_pdf(response,
        stylesheets=[weasyprint.CSS(settings.STATIC_ROOT) + 'css/pdf.css'])
    return response



"""CREATION FICHE FACTURE ET AFFICHAGE SUCCESS"""

class FactureCreate(CreateView):
    model = Facture
    form_class = FactureForm
    template_name = 'facture/facture_form.html'
    success_url = None
    
    def get_form(self):
        form = super().get_form()
        form.fields['date_debut'].widget = DatePickerInput().start_of('facture date')
        form.fields['date_echeance'].widget = DatePickerInput().end_of('facture date')
        form.fields['date_prestation'].widget = DatePickerInput().end_of('facture date')
        return form




def facture_create(request):

    #if id:
    #    facture = Facture.objects.get(pk=id)
    #else:
    facture = Facture()

    facture_form = FactureForm(instance=facture)

    FactureFormSet = inlineformset_factory(Facture, 
        PrestToFact, fields=('__all__'), 
        can_delete=True, extra=1)
    formset = FactureFormSet(instance=facture)

    if request.method == "POST":
        facture_form = FactureForm(request.POST)

        #if id:
        #    facture_form = FactureForm(request.POST, instance=facture)

        formset = FactureForm(request.POST)

        if facture_form.is_valid():
            created_facture = facture_form.save(commit=False)
            formset = FactureFormSet(request.POST, instance=created_facture)

            if formset.is_valid():
                created_facture.save()
                formset.save()
                return HttpResponseRedirect(created_facture.get_absolute_url())

    return render(request, template_name="facture/facture2.html", context={
        "facture_form":facture_form,
        "formset": formset,
       
    })            

    

class FactureView(DetailView):
    model = Facture

"""EDITER ET EFFACER FACTURE"""

class FactureUpdate(UpdateView):
    model = Facture
    fields = "__all__"



class FactureDelete(DeleteView):
    model = Facture
    success_url = reverse_lazy('facture_list')






"""CREATION FICHE CLIENT ET AFFICHAGE SUCCESS"""

class ClientCreate(CreateView):
    model = Client
    fields = '__all__'

class ClientView(DetailView):
    model = Client


"""EDITER ET EFFACER CLIENT"""

class ClientUpdate(UpdateView):
    model = Client
    fields = '__all__'

class ClientDelete(DeleteView):
    model = Client
    success_url = reverse_lazy('client_list')




"""CREATION FICHE PRESTATAIRE ET AFFICHAGE SUCCESS"""

class PrestataireCreate(CreateView):
    model = Prestataire
    fields = '__all__'

class PrestataireView(DetailView):
    model = Prestataire


"""EDITER ET EFFACER PRESTATAIRE"""

class PrestataireUpdate(UpdateView):
    model = Prestataire
    fields = '__all__'

class PrestataireDelete(DeleteView):
    model = Prestataire
    success_url = reverse_lazy('prestataire_list')


