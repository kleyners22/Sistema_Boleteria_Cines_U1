from django.urls import path

from .views import(PeliculaListView,
                SalaListView,
                CarteleraListView,
                ProyectarPeliculaListView
                )
urlpatterns= [
    path('pelicula/',PeliculaListView.as_view(),name = 'pelicula'),
    path('sala/',SalaListView.as_view(),name = 'sala'),
    path('cartelera/',CarteleraListView.as_view(),name = 'cartelera'),
    path('proyectar_pelicula/', ProyectarPeliculaListView.as_view(), name='proyectar_pelicula'),
    ]
