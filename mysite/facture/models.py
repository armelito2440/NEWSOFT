from django.db import models
from django.conf import settings
from django.forms import ModelForm
from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


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
    ENTR =[]
    ANNUELLE = 'ANNU'
    MENSUELLE = 'MENS'
    PONCTUELLE = 'PONC'
    TYPE_FACTURE_CHOICES =(
        (ANNUELLE, 'Annuelle'),
        (MENSUELLE, 'Mensuelle'),
        (PONCTUELLE, 'Ponctuelle')
        )
    type_facture = models.CharField(max_length=4,
        choices = TYPE_FACTURE_CHOICES,
        default= PONCTUELLE,
        verbose_name ='Type facture'
    ) 

    client= models.ForeignKey('Client', on_delete=models.CASCADE)
    prestataire = models.ForeignKey('Prestataire', on_delete=models.CASCADE) 
    ref_fact = models.DateField(default=timezone.now)
    # type_facture = models.CharField(max_length=50)
    date_debut = models.DateField()
    date_echeance = models.DateField()
    intitule = models.CharField(max_length=250)
    date_prestation = models.DateField()
    descriptif = models.TextField(blank=True, null=True)
    quantite = models.IntegerField (default = 0)
    prix_unitaire = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2)
    prix_HT = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2 )
    prix_TTC = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2)
    


    def get_absolute_url(self):
        return reverse("facture_detail", kwargs={"pk": self.pk})
    
    @classmethod
    def pourPDF(cls, request, Facture_id):
        facture = get_object_or_404(Facture, id=Facture_id)
        prixHT = facture.quantite * facture.prix_unitaire
        prixTTC = prixHT * (1 + facture.prestataire.TVA / 100)
        dontTVA = prixHT * facture.prestataire.TVA / 100
        echeance_12 = prixTTC / 12
        mois_1_echeance = facture.ref_fact.month
        dict_mois = {
            "1": "Janvier",
            "2": "Février",
            "3": 'Mars',
            "4": "Avril",
            "5": "Mai",
            "6": "Juin",
            "7": "Juillet",
            "8": "Aout",
            "9": "Septembre",
            "10": "Octobre",
            "11": "Novembre",
            "12": "Décembre"
            }
        lst_ech_g = []
        lst_ech_d = []    
        
        for i in range(12):
            m = mois_1_echeance + i
            if m > 12:
                m -= 12
            mois = dict_mois[str(m)]
            if i < 6:   
                lst_ech_g.append(mois)
            else:
                lst_ech_d.append(mois)

        lst_ech = zip(lst_ech_g, lst_ech_d)

        context ={
            'facture': facture,
            'Prix_HT': prixHT,
            'Prix_TTC': prixTTC,
            'DontTVA': dontTVA, 
            'Echeance_12': echeance_12,
            'liste_Echeance': lst_ech,
            
        }
        return context
        
