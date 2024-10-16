# core/urls.py

from django.urls import path
from .views import login_view, monitoramento_view, fornecedores_view, logout_view, cadastrar_fornecedor

app_name = 'core'

urlpatterns = [
    path('', login_view, name='login'),
    path('monitoramento/', monitoramento_view, name='monitoramento'),
    path('fornecedores/', fornecedores_view, name='fornecedores'),
    path('logout/', logout_view, name='logout'),
    path('fornecedores/cadastrar_fornecedor/', cadastrar_fornecedor, name='cadastrar_fornecedor'),

]
