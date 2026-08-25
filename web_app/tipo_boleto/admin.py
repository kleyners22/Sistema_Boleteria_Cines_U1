from django.contrib import admin
from model.models import TipoBoleto


class TipoBoletoAdmin(admin.ModelAdmin):
    list_display = (
        'id_tipo_boleto',
        'nombre'
    )
    search_fields = (
        'nombre',
    )


admin.site.register(TipoBoleto, TipoBoletoAdmin)