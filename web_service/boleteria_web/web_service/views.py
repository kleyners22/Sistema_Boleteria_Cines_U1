from django.shortcuts import render
from rest_framework.generics import(
    ListAPIView,
    RetrieveAPIView
)   
from .models import(Pelicula,Sala,Cartelera,ProyectarPelicula)

from .serializers import(PeliculaSerializer,SalaSerializer,CarteleraSerializer,ProyectarPeliculaSerializer)

class PeliculaListView(ListAPIView):
    serializer_class = PeliculaSerializer

    def get_queryset(self):
        ids_proyectados = ProyectarPelicula.objects.distinct('id_pelicula')
        return Pelicula.objects.filter(id_pelicula__in=ids_proyectados)


class SalaListView(ListAPIView):
    serializer_class = SalaSerializer

    def get_queryset(self):
        return Sala.objects.all()


class CarteleraListView(ListAPIView):
    serializer_class = CarteleraSerializer

    def get_queryset(self):
        return Cartelera.objects.all()


class ProyectarPeliculaListView(ListAPIView):
    serializer_class = ProyectarPeliculaSerializer

    def get_queryset(self):
        queryset = ProyectarPelicula.objects.all()
        id_pelicula = self.request.query_params.get('id_pelicula')
        if id_pelicula:
            try:
                queryset = queryset.filter(id_pelicula=int(id_pelicula))
            except (ValueError, TypeError):
                return ProyectarPelicula.objects.none()
        return queryset


# Create your views here.
