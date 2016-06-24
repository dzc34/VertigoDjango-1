from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from .models import Adherent, Contact, Adhesion, Materiel, Emprunt


class ContactInline(admin.TabularInline):
    model = Contact
    extra = 0


class AdhesionInline(admin.TabularInline):
    model = Adhesion
    extra = 0


class EmpruntInline(admin.TabularInline):
    model = Emprunt
    extra = 0


class AdherentAdmin(ImportExportActionModelAdmin):
    list_display = ('prenom', 'nom', '_telephone', 'email', '_est_inscrit')

    fieldsets = [
        ('Fiche personnelle', {'fields': ['nom', 'prenom', 'telephone', 'email', 'anniversaire']}),
    ]
    inlines = [ContactInline, AdhesionInline]
    # empty_value_display = 'nc'


class MaterielAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'remarque', 'etat', '_delai', '_emprunteur')
    # list_editable = ('_emprunteur', )

    fieldsets = [
        (None, {'fields': ['description', 'identifiant', 'remarque', 'etat']}),
        ('Informations EPI', {'fields': ['date_achat', 'magasin', 'marque', 'modele', 'couleur', 'num_serie',
                                         'date_fabrication']}),
    ]
    inlines = [EmpruntInline, ]


class EmpruntAdmin(admin.ModelAdmin):
    list_display = ('materiel_id', 'date_emprunt', 'adherent_id')
    list_editable = ('adherent_id', )


admin.site.register(Adherent, AdherentAdmin)
admin.site.register(Materiel, MaterielAdmin)
admin.site.register(Emprunt, EmpruntAdmin)
