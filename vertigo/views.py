from django.shortcuts import render
from django.http import HttpResponse
from django.utils import timezone
from django.template import defaultfilters

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm

from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import phonenumbers

from .models import Adherent, Emprunt


def gestion_materiel(request):
    liste_du_materiel = Emprunt.objects.all().distinct('materiel_id')
    context = {'liste_du_materiel': liste_du_materiel}
    return render(request, 'vertigo/materiel.html', context)


def pdf_adherents(request):
    if request.user.is_authenticated():
        liste_des_adherents = Adherent.objects.all()  # todo: filtrer seulement les adhérents en cours

        response = HttpResponse(content_type='application/pdf')
        filename = 'adherents-vertigo-{}.pdf'.format(timezone.now())
        response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

        # polices d'écriture
        pdfmetrics.registerFont(TTFont('EffraLight', 'effra_std_lt-webfont.ttf'))
        pdfmetrics.registerFont(TTFont('EffraMedium', 'effra_std_md-webfont.ttf'))
        pdfmetrics.registerFont(TTFont('King', 'KIN668.ttf'))

        # paramètres du PDF
        page = canvas.Canvas(response, pagesize=A4)
        page.setTitle('Liste des adhérents')
        page.setAuthor('Association Vertigo')
        page.setCreator('Django 1.9')

        # entête
        page.setFont('EffraMedium', 20)
        page.drawString(1.5*cm, 28*cm, 'LISTE DES ADHERENTS')
        page.setFont('EffraLight', 10)
        page.drawString(1.5*cm, 27.6*cm, 'Extraction du {}'.format(defaultfilters.date(timezone.now(), 'l j F Y')))

        def _pied_de_page():
            logo = '/home/remi/GitHub/VertigoDjango/static/img/logo.jpg'
            page.drawImage(logo, 16.5*cm, 1.1*cm, width=100, height=50)  # 16.5  0.8
            page.setFont('King', 10)
            page.drawString(1.5*cm, 2*cm, 'Association Vertigo - escalade, canyoning, randonnée')
            page.setLineWidth(0.5)
            page.line(1.5*cm, 1.8*cm, 16*cm, 1.8*cm)  # 14.8
            page.setFont('King', 8)
            page.drawString(1.5*cm, 1.4*cm, 'Cet annuaire est distribué uniquement aux adhérents de l\'association.')
            page.drawString(1.5*cm, 1.0*cm, 'Toute redistribution ou usage en dehors du cadre de l\'association est interdit.')

        _pied_de_page()

        def _entete_de_liste(bottom):
            page.setFont('EffraMedium', 10)
            page.drawString(8*cm, bottom*cm, 'E-MAIL')
            page.drawString(14*cm, bottom*cm, 'TELEPHONE')

        _entete_de_liste(26)

        page.setFont('EffraLight', 10)
        y = 25.5
        for adh in liste_des_adherents:
            page.drawString(1.5*cm, y*cm, '{} {}'.format(adh.prenom, adh.nom))
            page.drawString(8*cm, y*cm, adh.email)
            if adh.telephone:
                page.drawString(14*cm, y*cm, phonenumbers.format_number(adh.telephone, phonenumbers.PhoneNumberFormat.NATIONAL))
            y += -0.5
            if y < 5:
                page.showPage()
                _entete_de_liste(28)
                _pied_de_page()
                page.setFont('EffraLight', 10)
                y = 27.5

        page.showPage()
        page.save()

        return response
    else:
        return render(request, 'vertigo/login_error.html')  # todo: améliorer la réponse visuelement


def pdf_materiel(request):
    liste_du_materiel = Emprunt.objects.all().distinct('materiel_id')

    response = HttpResponse(content_type='application/pdf')
    filename = 'adherents-vertigo-{}.pdf'.format(timezone.now())
    response['Content-Disposition'] = 'attachment; filename={}'.format(filename)

    # polices d'écriture
    pdfmetrics.registerFont(TTFont('EffraLight', 'effra_std_lt-webfont.ttf'))
    pdfmetrics.registerFont(TTFont('EffraMedium', 'effra_std_md-webfont.ttf'))
    pdfmetrics.registerFont(TTFont('King', 'KIN668.ttf'))

    # paramètres du PDF
    page = canvas.Canvas(response, pagesize=A4)
    page.setTitle('Liste du matériel')
    page.setAuthor('Association Vertigo')
    page.setCreator('Django 1.9')

    # entête
    page.setFont('EffraMedium', 20)
    page.drawString(1.5*cm, 28*cm, 'LISTE DU MATERIEL')
    page.setFont('EffraLight', 10)
    page.drawString(1.5*cm, 27.6*cm, 'Extraction du {}'.format(defaultfilters.date(timezone.now(), 'l j F Y')))

    def _pied_de_page():
        logo = '/home/remi/GitHub/VertigoDjango/static/img/logo.jpg'
        page.drawImage(logo, 16.5*cm, 1.1*cm, width=100, height=50)  # 16.5  0.8
        page.setFont('King', 10)
        page.drawString(1.5*cm, 2*cm, 'Association Vertigo - escalade, canyoning, randonnée')
        page.setLineWidth(0.5)
        page.line(1.5*cm, 1.8*cm, 16*cm, 1.8*cm)  # 14.8
        page.setFont('King', 8)
        page.drawString(1.5*cm, 1.4*cm, 'Cet document est issu du système d\'information de l\'association Vertigo.')
        page.drawString(1.5*cm, 1.0*cm, 'Toute redistribution ou usage en dehors du cadre de l\'association est interdit.')

    _pied_de_page()

    def _entete_de_liste(bottom):
        page.setFont('EffraMedium', 10)
        page.drawString(1.5*cm, bottom*cm, 'MATERIEL')
        page.drawString(6*cm, bottom*cm, 'DATE D\'EMPRUNT')
        page.drawString(12*cm, bottom*cm, 'EMPRUNTEUR')

    _entete_de_liste(26)

    page.setFont('EffraLight', 10)
    y = 25.5
    for item in liste_du_materiel:
        page.drawString(1.5*cm, y*cm, '{}'.format(item.materiel_id))
        page.drawString(6*cm, y*cm, '{}'.format(item.date_emprunt))
        page.drawString(12*cm, y*cm, '{}'.format(item.adherent_id))
        y += -0.5
        if y < 5:
            page.showPage()
            _entete_de_liste(28)
            _pied_de_page()
            page.setFont('EffraLight', 10)
            y = 27.5

    page.showPage()
    page.save()

    return response
