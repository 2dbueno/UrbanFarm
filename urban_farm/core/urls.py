from django.urls import path
from .views import (
    LoginView, MonitoramentoView, FornecedoresView, LogoutView, 
    CadastrarFornecedorView, BuscarFornecedorView, EditarFornecedorView  # Importar a view correta
)

app_name = 'core'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('monitoramento/', MonitoramentoView.as_view(), name='monitoramento'),
    path('fornecedores/', FornecedoresView.as_view(), name='fornecedores'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('buscar_fornecedor/<int:fornecedor_id>/', BuscarFornecedorView.as_view(), name='buscar_fornecedor'),
    path('fornecedores/cadastrar_fornecedor/', CadastrarFornecedorView.as_view(), name='cadastrar_fornecedor'),
    path('fornecedores/editar/<int:fornecedor_id>/', EditarFornecedorView.as_view(), name='editar_fornecedor'),  # Corrigir a rota
]
