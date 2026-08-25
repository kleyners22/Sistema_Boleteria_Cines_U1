# cliente/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # ── App boleto ──
    path('boletos/', include('boleto.urls')),
]