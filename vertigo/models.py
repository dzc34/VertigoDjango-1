from django.db import models
from django.utils import timezone
from phonenumber_field.modelfields import PhoneNumberField
import phonenumbers


class Adherent(models.Model):
    """
        Table contenant toutes les infos concernant un adhérent
    """

    nom = models.CharField('nom', max_length=100)
    prenom = models.CharField('prénom', max_length=100)
    email = models.EmailField('email', max_length=254, blank=True)
    telephone = PhoneNumberField('téléphone', blank=True)
    anniversaire = models.DateField('date de naissance', blank=True, null=True)

    def _telephone(self):
        if self.telephone:
            return phonenumbers.format_number(self.telephone, phonenumbers.PhoneNumberFormat.NATIONAL)

    def _est_inscrit(self):
        value = Adhesion.objects.filter(adherent_id=self.id).latest('annee')
        if value.paiement != 'attente' and value.certificat is True and value.annee >= timezone.now().year - 1:
            return True
        else:
            return False
    _est_inscrit.boolean = True
    _est_inscrit.short_description = 'Inscription'

    def __str__(self):
        return '{} {}'.format(self.prenom, self.nom)

    class Meta:
        verbose_name = 'adhérent'
        verbose_name_plural = 'adhérents'
        ordering = ['prenom']


class Contact(models.Model):
    """
        Table qui relie un ou plusieurs contact en cas d'urgence à un adhérent
    """

    adherent_id = models.ForeignKey(Adherent)

    nom = models.CharField('nom', max_length=100, blank=True)
    prenom = models.CharField('prénom', max_length=100, blank=True)
    telephone = PhoneNumberField('téléphone', help_text='Au format international, ex: +33434170166')

    def __str__(self):
        return '{} {}'.format(self.prenom, self.nom)

    class Meta:
        verbose_name = 'contact en cas d\'urgence'
        verbose_name_plural = 'contacts en cas d\'urgence'


class Adhesion(models.Model):
    """
        Renseignements relatifs à l'adhésion en cours pour un adhérent
    """

    CHOIX_ANNEE = []
    for an in range(timezone.now().year, 1987, -1):
        CHOIX_ANNEE.append((an, '{} - {}'.format(an, an+1)))

    CHOIX_PAIEMENT = (
        ('attente', 'En attente de paiement...'),
        ('cheque', 'Chèque'),
        ('especes', 'Espèces'),
    )

    adherent_id = models.ForeignKey(Adherent)

    annee = models.IntegerField('année', choices=CHOIX_ANNEE, default=timezone.now().year)
    paiement = models.CharField('paiement', max_length=10, choices=CHOIX_PAIEMENT, default='attente')
    certificat = models.BooleanField('certificat médical', default=False)
    date = models.DateField('date d\'inscription', default=timezone.now)

    # @property
    # def _statut(self):
    #    if self.paiement != 'attente' and self.certificat is True:
    #        return True
    #    else:
    #        return False
    # _statut.boolean = True
    # statut = property(_statut)

    def __str__(self):
        return str(self.annee)

    class Meta:
        verbose_name = 'adhésion'
        verbose_name_plural = 'adhésions'
        ordering = ['-annee']


class Materiel(models.Model):
    """
        Toutes les informations concernant un élément de matériel
    """

    CHOIX_ETAT = (
        ('neuf', 'Neuf'),
        ('normal', 'Normal'),
        ('especes', 'A surveiller !'),
        ('reforme', 'Réformé'),
    )

    description = models.CharField('description', max_length=100)
    identifiant = models.IntegerField('identifiant', blank=True)
    remarque = models.CharField('remarques', max_length=250, blank=True)
    etat = models.CharField('etat', choices=CHOIX_ETAT, max_length=10, default='normal')

    # infos EPI
    date_achat = models.DateField('date d\'achat', blank=True, null=True)
    marque = models.CharField('marque', max_length=100, blank=True)
    modele = models.CharField('modèle', max_length=100, blank=True)
    couleur = models.CharField('couleur', max_length=100, blank=True)
    magasin = models.CharField('magasin', max_length=100, blank=True)
    num_serie = models.CharField('numéro de série', max_length=100, blank=True)
    date_fabrication = models.DateField('date de fabrication', blank=True, null=True)

    def _emprunteur(self):
        return Emprunt.objects.filter(materiel_id=self.id).latest('date_emprunt')

    def _delai(self):
        return Emprunt.objects.filter(materiel_id=self.id).latest('date_emprunt').date_emprunt

    def __str__(self):
        return '{} n°{}'.format(self.description, self.identifiant)

    class Meta:
        verbose_name = 'fiche matériel'
        verbose_name_plural = 'fiches matériel'
        ordering = ['identifiant']


class Emprunt(models.Model):
    """
        Date et personne qui réalise un emprunt de matériel
    """

    materiel_id = models.ForeignKey(Materiel)
    adherent_id = models.ForeignKey(Adherent)
    date_emprunt = models.DateField('date d\'emprunt', default=timezone.now)

    def __str__(self):
        return str(self.adherent_id)

    class Meta:
        verbose_name = 'emprunt'
        verbose_name_plural = 'emprunts'
