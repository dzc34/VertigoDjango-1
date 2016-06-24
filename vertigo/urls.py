from django.conf.urls import url
from vertigo import views

urlpatterns = [
    url(r'^materiel', views.gestion_materiel, name='materiel'),
    url(r'^pdf_matos/', views.pdf_materiel),
    url(r'^pdf_adherents/', views.pdf_adherents)
]
