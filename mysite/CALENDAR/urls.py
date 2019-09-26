from django.contrib import admin, auth
from django.urls import path, include
from django.conf.urls import url
from . import views
from . views import CreateView

urlpatterns = [
    path('letter/', views.LetterCreateView.as_view(), name= "letter create" ),
]