from django.contrib import admin
from model.models import Boleto


class BoletoAdmin(admin.ModelAdmin):
    list_display = (
        'numero_boleto',
        'cedula_cliente',
        'id_tipo_boleto',
        'id_pelicula',
        'hora',
        'fecha',
        'precio',
        'id_cajero',
        'asiento',
        'numero_sala',       
    )
    search_fields = (
        'numero_boleto',
        'id_pelicula'
    )


admin.site.register(Boleto, BoletoAdmin)