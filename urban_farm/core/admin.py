# core/admin.py

from django.contrib import admin
from .models import Produto, Pedido, Perfil

admin.site.register(Produto)
admin.site.register(Pedido)
admin.site.register(Perfil)
