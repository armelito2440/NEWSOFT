#coding: utf-8 

from django.contrib import admin
from django.urls import path
from . import views

# from .views import facture, client, prestataire
from .views import FactureView, PrestataireView, ClientView
from .views import UpdateView, DeleteView 
from .views import FactureCreate, FactureView, FactureUpdate, FactureDelete, FactureSearchList
# from .views import HelloPDFView

urlpatterns = [
    path ('facture/', views.FactureCreate.as_view(), name='facture_form'),
    path ('facture_list/', views.FactureSearchList.as_view(), name='facture_list'),
    path ('facture_detail/<int:pk>',views.FactureView.as_view(), name='facture_detail'),
    path ('facture_update_form/<int:pk>',views.FactureUpdate.as_view(), name='facture_update_form'),
    path ('facture_check_delete/<int:pk>',views.FactureDelete.as_view(), name='facture_check_delete'),

   
    
    # path ('hello/',views.HelloPDFView.as_view(), name='hello'),
    # path ('facture_detail_PDF/<int:pk>',views.HelloPDFView.as_view(), name='facture_detail_PDF'),

    path ('client/', views.ClientCreate.as_view(), name='client_form'),
    path ('client_list/', views.client, name='client_list'),
    path ('client_detail/<int:pk>',views.ClientView.as_view(), name='client_detail'),
    path ('client_update_form/<int:pk>',views.ClientUpdate.as_view(), name='client_update_form'),
    path ('client_check_delete/<int:pk>',views.ClientDelete.as_view(), name='client_check_delete'),




    path ('prestataire/', views.PrestataireCreate.as_view(), name='prestataire_form'),
    path ('prestataire_list/', views.prestataire, name='prestataire_list'),
    path ('prestataire_detail/<int:pk>',views.PrestataireView.as_view(), name='prestataire_detail'),
    path ('prestataire_update_form/<int:pk>',views.PrestataireUpdate.as_view(), name='prestataire_update_form'),
    path ('prestataire_check_delete/<int:pk>',views.PrestataireDelete.as_view(), name='prestataire_check_delete'),


]