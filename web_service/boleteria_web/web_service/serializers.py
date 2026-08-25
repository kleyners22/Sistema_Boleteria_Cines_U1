from rest_framework import serializers


class SalaSerializer(serializers.Serializer):
    numero_sala = serializers.IntegerField()
    asientos = serializers.IntegerField()
    estado = serializers.CharField(max_length=9)

    def to_representation(self, instance):
        return {
            'numero_sala': instance.numero_sala,
            'asientos': instance.asientos,
            'estado': instance.estado,
        }


class PeliculaSerializer(serializers.Serializer):
    id_pelicula = serializers.IntegerField()
    id_cartelera = serializers.IntegerField()
    titulo = serializers.CharField(max_length=50)
    duracion = serializers.IntegerField()
    clasificacion = serializers.CharField(max_length=4, required=False)
    genero = serializers.CharField(max_length=20)

    def to_representation(self, instance):
        return {
            'id_pelicula': instance.id_pelicula,
            'id_cartelera': instance.id_cartelera,
            'titulo': instance.titulo,
            'duracion': instance.duracion,
            'clasificacion': instance.clasificacion,
            'genero': instance.genero,
        }


class CarteleraSerializer(serializers.Serializer):
    id_cartelera = serializers.IntegerField()
    fecha_inicio = serializers.DateField()
    fecha_fin = serializers.DateField()
    nombre = serializers.CharField(max_length=100, required=False)

    def to_representation(self, instance):
        return {
            'id_cartelera': instance.id_cartelera,
            'fecha_inicio': instance.fecha_inicio,
            'fecha_fin': instance.fecha_fin,
            'nombre': instance.nombre,
        }


class ProyectarPeliculaSerializer(serializers.Serializer):
    id_proyectar_pelicula = serializers.IntegerField()
    id_pelicula = serializers.IntegerField()
    numero_sala = serializers.IntegerField()
    fecha = serializers.DateField()
    hora = serializers.CharField(max_length=8)

    def to_representation(self, instance):
        return {
            'id_proyectar_pelicula': instance.id_proyectar_pelicula,
            'id_pelicula': instance.id_pelicula,
            'numero_sala': instance.numero_sala,
            'fecha': instance.fecha,
            'hora': instance.hora,
        }
