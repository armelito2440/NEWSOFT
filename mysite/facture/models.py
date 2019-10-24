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
    
      
class Prestation(models.Model):

    intitule = models.CharField(max_length=250)
    descriptif = models.TextField(blank=True, null=True)
    
    def get_absolute_url(self):
        return reverse("prestation", kwargs={"pk": self.pk})

    def __str__(self):
        return (self.intitule)   




""" 3 - FACTURE"""

class Facture(models.Model):

    
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
    date_debut = models.DateField()
    date_echeance = models.DateField()
    date_prestation = models.DateField()
    nombre_echeance = models.SmallIntegerField(default=1)
    
    


    def get_absolute_url(self):
        return reverse("facture_detail", kwargs={"pk": self.pk})
    
    @classmethod
    def pourPDF(cls, request, Facture_id):
        facture = get_object_or_404(Facture, id=Facture_id)
        prixHT = PrestToFact.total_HT(fact=Facture_id)
        prixTTC = prixHT * (1 + facture.prestataire.TVA / 100)
        dontTVA = prixHT * facture.prestataire.TVA / 100
        echeances_mt = prixTTC / facture.nombre_echeance
        nombre_echeance = facture.nombre_echeance
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
        lst_ech = []
        prem_ech=""    
        
        k=1
        if facture.nombre_echeance % 2 == 0:
            n = nombre_echeance // 2
            for i in range(n): 
                m_g = mois_1_echeance + i
                if m_g > 12:
                    m_g -= 12
                mois_g = dict_mois[str(m_g)]
                lst_ech_g.append(mois_g)
                m_d = m_g + nombre_echeance // 2 
                if m_d > 12:
                    m_d -= 12
                mois_d = dict_mois[str(m_d)]
                lst_ech_d.append(mois_d)
            lst_ech = zip(lst_ech_g, lst_ech_d)    
        else:
            N = nombre_echeance // 2 + 1
            for i in range(N): 
                m_g = mois_1_echeance + i
                if m_g > 12:
                    m_g -= 12
                mois_g = dict_mois[str(m_g)]
                lst_ech_g.append(mois_g)
        
                if k < nombre_echeance // 2 + 1:
                    m_d = m_g + nombre_echeance // 2 + 1
                    if m_d > 12:
                        m_d -= 12
                    mois_d = dict_mois[str(m_d)]
                    lst_ech_d.append(mois_d)
                    k +=1
            prem_ech = lst_ech_g.pop(0)
            lst_ech = zip(lst_ech_g, lst_ech_d)
        
        context ={
            'facture': facture,
            'Prix_HT': prixHT,
            'Prix_TTC': prixTTC,
            'DontTVA': dontTVA, 
            'Echeance_MT': echeances_mt,
            'liste_Echeance': lst_ech,
            'liste_D': lst_ech_d,
            'liste_G': lst_ech_g,
            'prem_ech': prem_ech,
        }
        return context
        
class PrestToFact(models.Model):
    
    fact = models.ForeignKey(Facture,
                             related_name="prestations",
                             on_delete=models.CASCADE)
    prest = models.ForeignKey(Prestation,
                              related_name="fact_prestations",
                              on_delete=models.CASCADE)
    quantite = models.IntegerField (default = 0, verbose_name='quant')
    prix_unitaire_HT = models.DecimalField(default = 0.00 , max_digits = 18 , decimal_places = 2)
    
    
    def __str__(self):
        return '{}'.format(self.id)

    def prix_HT(self):
        calc = self.quantite * self.prix_unitaire_HT
        prix_HT = getattr(calc)
        return prix_HT    
        
    @classmethod
    def total_HT(cls, fact):
        lst = PrestToFact.objects.all().filter(fact_id=fact)
        total_HT_Fact = 0
        total_HT_Fact = sum(p['prix_unitaire_HT'] * p['quantite'] for p in lst.values())
        return total_HT_Fact
        
        
