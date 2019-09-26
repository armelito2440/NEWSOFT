from django.conf import settings
from django.forms import ModelForm
from django.db import models
from django.urls import reverse
from django.utils import timezone
from decimal import Decimal

# Create your models here.


""" 1 - PRESTATAIRE"""

class Prestataire(models.Model):
    logo = models.ImageField(null = True, blank = True, upload_to ='logo')
    nom = models.CharField(max_length=50)
    adresse = models.CharField(max_length=250)
    code_postal = models.CharField(max_length=10)
    ville = models.CharField(max_length=50)
    telephone = models.CharField(max_length=16,blank=True)
    TVA = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2)
    calc_tva_seule = models.CharField(max_length=16,blank=True)
    calc_tva_appli = models.CharField(max_length=16,blank=True)
    email = models.EmailField(max_length=254, blank=True)
    siret = models.CharField(max_length=14, blank=True)
    codenaf = models.CharField(max_length=8, blank=True)
    mention_legale = models.TextField(blank=True)
    rib = models.CharField(max_length=100, blank=True)
    entete = models.TextField(blank=True)

    def __str__(self):
        return (self.nom)


    def get_absolute_url(self):
            return reverse("prestataire_detail", kwargs={"pk": self.pk})



""" 2 - CLIENT"""


class Client(models.Model):
    nom_societe = models.CharField(max_length=250)
    nom_contact_client = models.CharField(max_length=250, blank=True)
    adresse = models.CharField(max_length=250,blank=True )
    code_postal = models.CharField(max_length=5, blank=True)
    ville = models.CharField(max_length=50,blank=True )
    telephone = models.CharField(max_length=16, blank=True)
    email = models.EmailField(max_length=254, blank=True)
    siret = models.CharField(max_length=14, blank=True)
    rib_iban = models.CharField(max_length=20, blank=True)

    def __str__(self):
        return (self.nom_societe)

    def get_absolute_url(self):
            return reverse("client_detail", kwargs={"pk": self.pk})
    
      


""" 3 - FACTURE"""

class Facture(models.Model):

    # TODO créer une liste de choix pour catégorie facture etc...
    # ENTR =[]
    # ANNUELLE = 'A'
    # MENSUELLE = 'M'
    # PONCTUELLE = 'P'
    # TYPE_FACTURE_CHOICES =(
    #     (ANNUELLE, 'Annuelle'),
    #     (MENSUELLE, 'Mensuelle'),
    #     (PONCTUELLE, 'Ponctuelle')
    #     )
    # type_facture = models.CharField(max_length=4,
    #     choices = TYPE_FACTURE_CHOICES,
    #     default= PONCTUELLE,
    #     verbose_name ='Type facture'
    # ) 

    client= models.ForeignKey('Client', on_delete=models.CASCADE)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.CASCADE) 
    ref_fact = models.DateField(default=timezone.now)
    type_facture = models.CharField(max_length=50)
    date_debut = models.DateField(auto_now=False, auto_now_add=False)
    date_echeance = models.DateField(auto_now=False, auto_now_add=False)
    intitule = models.CharField(max_length=250)
    date_prestation = models.DateField(auto_now=False, auto_now_add=False)
    descriptif = models.TextField(blank=True, null=True)
    quantite = models.IntegerField (default = 0)
    prix_unitaire = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2)
    prix_HT = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2 )
    prix_TTC = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2)
    


    def get_absolute_url(self):
        return reverse("facture_detail", kwargs={"pk": self.pk})
    
        
    


'''
class Image(models.Model):
    name= models.CharField(max_length=500)
    imagefile= models.ImageField(upload_to='logo/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.imagefile)


    def get_absolute_url(self):
        return reverse("facture_detail", kwargs={"pk": self.pk})
'''