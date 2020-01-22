# accueil/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('baseSocle/<int:pk>/', views.baseSocle, name='baseSocle'),
    path('search_bar/', views.search_bar, name='search_bar'),
    path('search_bar/', views.search_bar, name='search_bar'),
  
]