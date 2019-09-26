from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render

@login_required
def index(request):

    send_mail('Hello from Spiderman',
    'Un nouveau mail est arrivé. Ceci est un message automatique',
    'facturation.nouveausoft@gmail.com',
    ['denechaud@lavache.com','armelitomac@gmail.com'],
    fail_silently=False)
    return render(request, 'send/index.html')
