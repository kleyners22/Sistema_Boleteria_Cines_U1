# boleto/urls.py

from django.urls import path
from boleto import views

urlpatterns = [
    path('',            views.index,             name='boletos-index'),
    path('carteleras/', views.listar_carteleras,  name='boletos-carteleras'),
    path('peliculas/',  views.listar_peliculas,   name='boletos-peliculas'),
    path('generar/',    views.generar_boleto,      name='boletos-generar'),
]