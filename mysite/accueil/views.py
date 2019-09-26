from django.shortcuts import render
from .models import Image
from .forms import ImageForm

# Create your views here.

def index(request):
    return render(request, 'accueil.html')

def baseSocle(request):
    return render(request, 'baseSocle.html')


def showimage(request):
    lastimage=Image.objects.last()
    imagefile=lastimage.imagefile
    form= ImageForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    context={'imagefile':imagefile,
             'form' : form
             }
    return render(request, 'prestataire_detail.html', context),
    return render(request, 'facture_detail.html', context)


