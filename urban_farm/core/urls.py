from django.urls import path
from .views import (
    LoginView, MonitoramentoView, FornecedoresView, LogoutView, 
    CadastrarFornecedorView, BuscarFornecedorView, EditarFornecedorView,
    BuscarFornecedorPorCNPJView, ProducaoView, FuncionariosView, 
    CadastrarFuncionarioView, BuscarFuncionarioView, EditarFuncionarioView,
    ClientesView, CadastrarClienteView, BuscarClienteView, EditarClienteView
)

app_name = 'core'

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('monitoramento/', MonitoramentoView.as_view(), name='monitoramento'),
    path('fornecedores/', FornecedoresView.as_view(), name='fornecedores'),
    path('producao/', ProducaoView.as_view(), name='producao'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('buscar_fornecedor/<int:fornecedor_id>/', BuscarFornecedorView.as_view(), name='buscar_fornecedor'),
    path('buscar_fornecedor/cnpj/<str:cnpj>/', BuscarFornecedorPorCNPJView.as_view(), name='buscar_fornecedor_cnpj'),
    path('fornecedores/cadastrar_fornecedor/', CadastrarFornecedorView.as_view(), name='cadastrar_fornecedor'),
    path('fornecedores/editar/<int:fornecedor_id>/', EditarFornecedorView.as_view(), name='editar_fornecedor'),
    
    path('funcionarios/', FuncionariosView.as_view(), name='funcionarios'),
    path('funcionarios/cadastrar/', CadastrarFuncionarioView.as_view(), name='cadastrar_funcionario'),
    path('funcionarios/<int:funcionario_id>/', BuscarFuncionarioView.as_view(), name='buscar_funcionario'),
    path('funcionarios/editar/<int:funcionario_id>/', EditarFuncionarioView.as_view(), name='editar_funcionario'),

    path('clientes/', ClientesView.as_view(), name='clientes'),
    path('clientes/cadastrar/', CadastrarClienteView.as_view(), name='cadastrar_cliente'),
    path('clientes/<int:cliente_id>/', BuscarClienteView.as_view(), name='buscar_cliente'),
    path('clientes/editar/<int:cliente_id>/', EditarClienteView.as_view(), name='editar_cliente'),
]