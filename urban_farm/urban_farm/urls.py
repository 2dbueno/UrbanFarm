# urban_farm/urls.py

# Configuração das URLs do projeto Django.
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls), # URL para acessar o painel administrativo do Django
    path('', include('core.urls')), # Inclui as URLs do aplicativo 'core'
    # Redireciona a requisição do favicon para o arquivo correspondente em STATIC_URL
    path('favicon.ico', RedirectView.as_view(url=settings.STATIC_URL + 'images/favicon.ico')),  # Redireciona o favicon
]
