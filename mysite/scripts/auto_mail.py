from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta

# from django.core.mail import send_mail  # I think this is right.
from django.core.mail import EmailMessage
import weasyprint
from io import BytesIO
from django.template.loader import render_to_string

from facture.models import Facture




def run():
   for facture in Facture.objects.all():
       diff = datetime.now().date() - facture.date_debut
       diff = diff.days

       if datetime.now().date() - timedelta(days=0) == facture.date_debut:
              print('message créé')
              # Create Message
              subject = "Facture de Tonton Jean-Luc {}".format(facture.id)
              message = "Votre facture est en pièce jointe"
              email = EmailMessage(subject,
                                   message,
                                   'jl062705@sfr.fr',
                                   [facture.client.email,],
                                   )
              # generate pdf
              request=""
              context = Facture.pourPDF(request, facture.id)
              html = render_to_string('facture/facture_detail_PDF.html',
                                   context)
              # enregistre pdf en mémoire                        
              out = BytesIO()
              weasyprint.HTML(string=html).write_pdf(out)

              # attach PDF file
              email.attach('facture_{}_{}.pdf'.format(facture.ref_fact, facture.id),
                            out.getvalue(),
                     'application/pdf')

              # send email
              email.send()
