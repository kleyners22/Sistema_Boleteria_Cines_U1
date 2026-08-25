from django.contrib import admin
from model.models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        'cedula_cliente',
        'nombres',
        'apellidos',
        'correo'
    )
    list_filter = ('cedula_cliente', 'apellidos')
    search_fields = ('cedula_cliente', 'nombres', 'apellidos')


admin.site.register(Cliente, ClienteAdmin)