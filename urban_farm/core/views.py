# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Fornecedor, Monitoramento, Planta, Funcionario, Cliente
from .forms import FornecedorForm, EnderecoForm, FuncionarioForm, ClienteForm

# Classe base para views relacionadas a fornecedores.
# Essa classe contém métodos comuns que serão reutilizados em outras views.
class BaseFornecedorView(View):
    def get_fornecedores_data(self, fornecedores):
        # Retorna um dicionário com dados dos fornecedores e informações do usuário.
        return {
            'fornecedores': list(fornecedores.values('id', 'nome_fantasia', 'cnpj', 'status')),
            'user_is_superuser': self.request.user.is_superuser,
        }

# View para o login do usuário.
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        # Se o usuário já estiver autenticado, redireciona para a página de monitoramento.
        if request.user.is_authenticated:
            return redirect('monitoramento/')
        return render(request, self.template_name)
    
    def post(self, request):
        # Autentica o usuário com base no username e password.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            # Faz o login do usuário caso não logado.
            login(request, user)
            return redirect('monitoramento/')
        else:
            # Se a autenticação falhar, retorna uma mensagem de erro.
            error_message = "Usuário ou senha inválidos. Contate seu superior."
            return render(request, self.template_name, {'error_message': error_message})

# View para exibir informações de monitoramento.
class MonitoramentoView(LoginRequiredMixin, View):
    template_name = 'monitoramento.html'

    def get(self, request):
        # Obtém o primeiro objeto de monitoramento e o passa para o template.
        monitoramento = Monitoramento.objects.first()
        return render(request, self.template_name, {'monitoramento': monitoramento})

# View para realizar logout do usuário.
class LogoutView(View):
    def get(self, request):
        logout(request)  # Realiza o logout do usuário.
        return redirect('core:login')  # Redireciona para a página de login.

# View para listar fornecedores.
class FornecedoresView(LoginRequiredMixin, BaseFornecedorView):
    template_name = 'fornecedores.html'

    def get(self, request):
        # Obtém todos os fornecedores e renderiza o template.
        fornecedores = Fornecedor.objects.all()
        form = FornecedorForm()
        endereco_form = EnderecoForm()
        return render(request, self.template_name, {
            'fornecedores': fornecedores,
            'form': form,
            'endereco_form': endereco_form
        })

# View para cadastrar um novo fornecedor.
class CadastrarFornecedorView(View):
    def post(self, request):
        # Processa o formulário de cadastro de fornecedor e endereço.
        fornecedor_form = FornecedorForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if fornecedor_form.is_valid() and endereco_form.is_valid():
            fornecedor = fornecedor_form.save(commit=False)  # Salva o fornecedor sem commit.
            endereco = endereco_form.save()  # Salva o endereço.
            fornecedor.endereco = endereco  # Associa o endereço ao fornecedor.
            fornecedor.save()  # Salva o fornecedor.

            return JsonResponse({
                'success': True,
                'fornecedor': {
                    'id': fornecedor.id,
                    'nome_fantasia': fornecedor.nome_fantasia,
                    'cnpj': fornecedor.cnpj,
                    'status': fornecedor.status,
                }
            })
        else:
            # Retorna erros de validação, se houver.
            errors = {**fornecedor_form.errors, **endereco_form.errors}
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)

    def get(self, request):
        # Renderiza o formulário de cadastro de fornecedor.
        return render(request, 'fornecedores.html', {
            'form': FornecedorForm(),
            'endereco_form': EnderecoForm(),
        })

# View para buscar um fornecedor específico por ID.
class BuscarFornecedorView(LoginRequiredMixin, BaseFornecedorView):
    def get(self, request, fornecedor_id):
        # Obtém o fornecedor pelo ID e seus dados de endereço.
        fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
        endereco = fornecedor.endereco

        return JsonResponse({
            'fornecedor': {
                'cnpj': fornecedor.cnpj,
                'status': fornecedor.status,
                'razao_social': fornecedor.razao_social,
                'nome_fantasia': fornecedor.nome_fantasia,
                'nome_representante': fornecedor.nome_representante,
            },
            'endereco': {
                'cep': endereco.cep,
                'endereco': endereco.endereco,
                'complemento': endereco.complemento,
                'cidade': endereco.cidade,
                'estado': endereco.estado,
                'bairro': endereco.bairro,
                'telefone': endereco.telefone,
                'email': endereco.email,
            },
            'user_has_permission': request.user.is_superuser
        })

# View para editar um fornecedor existente.
class EditarFornecedorView(LoginRequiredMixin, UserPassesTestMixin, BaseFornecedorView):
    def test_func(self):
        # Verifica se o usuário é superusuário.
        return self.request.user.is_superuser

    def get(self, request, fornecedor_id):
        # Obtém o fornecedor pelo ID e renderiza o formulário de edição.
        fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
        form = FornecedorForm(instance=fornecedor)
        return render(request, 'core/fornecedor.html', {'form': form, 'fornecedor': fornecedor})

    def post(self, request, fornecedor_id):
        # Processa o formulário de edição do fornecedor.
        fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
        fornecedor_form = FornecedorForm(request.POST, instance=fornecedor)

        if fornecedor_form.is_valid():
            fornecedor_form.save()
            return JsonResponse({'success': True})
        else:
            # Retorna erros de validação, se houver.
            errors = fornecedor_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)

# View para buscar fornecedores por CNPJ.
class BuscarFornecedorPorCNPJView(LoginRequiredMixin, BaseFornecedorView):
    def get(self, request, cnpj):
        # Busca fornecedores com CNPJ que contenha a string fornecida.
        fornecedores = Fornecedor.objects.filter(cnpj__icontains=cnpj)
        if not fornecedores.exists():
            return JsonResponse({'fornecedores': []}, status=404)

        data = self.get_fornecedores_data(fornecedores)
        return JsonResponse(data)

# View para deletar um fornecedor.
class DeletarFornecedorView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        # Verifica se o usuário é superusuário.
        return self.request.user.is_superuser

    def post(self, request, fornecedor_id):
        # Deleta o fornecedor pelo ID.
        fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
        fornecedor.delete()
        return JsonResponse({'success': True})

class ProducaoView(LoginRequiredMixin, View):
    template_name = 'producao.html'

    def get(self, request):
        # Obtém todas as plantas do banco de dados
        plantas = Planta.objects.all()
        
        # Renderiza a template com o contexto das plantas
        return render(request, self.template_name, {'plantas': plantas})
    
class FuncionariosView(LoginRequiredMixin, View):
    template_name = 'funcionarios.html'

    def get(self, request):
        funcionarios = Funcionario.objects.all()
        form = FuncionarioForm()
        endereco_form = EnderecoForm()
        return render(request, self.template_name, {
            'funcionarios': funcionarios,
            'form': form,
            'endereco_form': endereco_form
        })

    def post(self, request):
        return redirect('core:cadastrar_funcionario')

class CadastrarFuncionarioView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            # Converte o status para boolean
            request.POST = request.POST.copy()
            request.POST['status'] = request.POST.get('status') == 'true'
            
            funcionario_form = FuncionarioForm(request.POST)
            endereco_form = EnderecoForm(request.POST)

            if funcionario_form.is_valid() and endereco_form.is_valid():
                endereco = endereco_form.save()
                funcionario = funcionario_form.save(commit=False)
                funcionario.endereco = endereco
                funcionario.save()

                return JsonResponse({
                    'success': True,
                    'funcionario': {
                        'id': funcionario.id,
                        'nome': funcionario.nome,
                        'cpf': funcionario.cpf,
                        'cargo': funcionario.cargo,
                        'status': funcionario.status,
                    }
                })
            else:
                errors = {}
                errors.update(funcionario_form.errors)
                errors.update(endereco_form.errors)
                return JsonResponse({
                    'success': False,
                    'errors': errors
                }, status=400)
                
        except Exception as e:
            return JsonResponse({
                'success': False,
                'errors': str(e)
            }, status=500)

class BuscarFuncionarioView(LoginRequiredMixin, View):
    def get(self, request, funcionario_id):
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        endereco = funcionario.endereco

        return JsonResponse({
            'funcionario': {
                'cpf': funcionario.cpf,
                'nome': funcionario.nome,
                'cargo': funcionario.cargo,
                'data_admissao': funcionario.data_admissao.strftime('%Y-%m-%d'),
                'salario': str(funcionario.salario),
                'status': funcionario.status,
            },
            'endereco': {
                'cep': endereco.cep,
                'endereco': endereco.endereco,
                'complemento': endereco.complemento,
                'cidade': endereco.cidade,
                'estado': endereco.estado,
                'bairro': endereco.bairro,
                'telefone': endereco.telefone,
                'email': endereco.email,
            }
        })

class EditarFuncionarioView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, funcionario_id):
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        form = FuncionarioForm(instance=funcionario)
        return render(request, 'funcionario.html', {'form': form, 'funcionario': funcionario})

    def post(self, request, funcionario_id):
        funcionario = get_object_or_404(Funcionario, id=funcionario_id)
        funcionario_form = FuncionarioForm(request.POST, instance=funcionario)

        if funcionario_form.is_valid():
            funcionario_form.save()
            return JsonResponse({'success': True})
        else:
            errors = funcionario_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)

class ClientesView(LoginRequiredMixin, View):
    template_name = 'clientes.html'

    def get(self, request):
        clientes = Cliente.objects.all()
        form = ClienteForm()
        endereco_form = EnderecoForm()
        return render(request, self.template_name, {
            'clientes': clientes,
            'form': form,
            'endereco_form': endereco_form
        })

    def post(self, request):
        return redirect('core:cadastrar_cliente')

class CadastrarClienteView(LoginRequiredMixin, View):
    def post(self, request):
        try:
            request.POST = request.POST.copy()
            status_value = request.POST.get('status') == 'on'  # 'on' se o checkbox estiver marcado
            request.POST['status'] = 1 if status_value else 0  # Define como 1 se True, caso contrário 0
            
            print("Dados recebidos:", request.POST)  # Log dos dados recebidos
            
            cliente_form = ClienteForm(request.POST)
            endereco_form = EnderecoForm(request.POST)

            if cliente_form.is_valid() and endereco_form.is_valid():
                endereco = endereco_form.save()
                cliente = cliente_form.save(commit=False)
                # Aqui, o status é definido a partir do formulário
                cliente.status = bool(request.POST['status'])  # Converte para booleano
                cliente.endereco = endereco
                cliente.save()

                return JsonResponse({
                    'success': True,
                    'cliente': {
                        'id': cliente.id,
                        'nome': cliente.nome,
                        'cpf': cliente.cpf,
                        'status': cliente.status,
                    }
                })
            else:
                errors = {}
                errors.update(cliente_form.errors)
                errors.update(endereco_form.errors)
                print("Erros de validação:", errors)  # Log dos erros de validação
                return JsonResponse({'success': False, 'errors': errors}, status=400)
                
        except Exception as e:
            print("Erro:", e)  # Log do erro
            return JsonResponse({'success': False, 'errors': str(e)}, status=500)

class BuscarClienteView(LoginRequiredMixin, View):
    def get(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, id=cliente_id)
        endereco = cliente.endereco

        return JsonResponse({
            'cliente': {
                'tipo': cliente.tipo,
                'cpf': cliente.cpf,
                'nome': cliente.nome,
                'status': cliente.status,
            },
            'endereco': {
                'cep': endereco.cep,
                'endereco': endereco.endereco,
                'complemento': endereco.complemento,
                'cidade': endereco.cidade,
                'estado': endereco.estado,
                'bairro': endereco.bairro,
                'telefone': endereco.telefone,
                'email': endereco.email,
            }
        })

class EditarClienteView(LoginRequiredMixin, UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, id=cliente_id)
        form = ClienteForm(instance=cliente)
        return render(request, 'cliente.html', {'form': form, 'cliente': cliente})

    def post(self, request, cliente_id):
        cliente = get_object_or_404(Cliente, id=cliente_id)
        cliente_form = ClienteForm(request.POST, instance=cliente)

        if cliente_form.is_valid():
            cliente_form.save()
            return JsonResponse({'success': True})
        else:
            errors = cliente_form.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)

from django.shortcuts import render
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.db import transaction
from .models import Venda, Cliente, ItemVenda
from .forms import VendaForm, ItemVendaFormSet

class VendasView(LoginRequiredMixin, View):
    template_name = 'vendas.html'

    def get(self, request):
        vendas = Venda.objects.all().order_by('-data_venda')
        return render(request, self.template_name, {
            'vendas': vendas,
            'form': VendaForm(),
        })

class BuscarClienteVendaView(LoginRequiredMixin, View):
    def get(self, request):
        tipo = request.GET.get('tipo')
        documento = request.GET.get('documento')
        
        try:
            if tipo == 'PF':
                cliente = Cliente.objects.filter(tipo='PF', cpf=documento).first()
                if cliente:
                    return JsonResponse({
                        'cliente': {
                            'nome': cliente.nome,
                            'cpf': cliente.cpf
                        }
                    })
            else:
                cliente = Cliente.objects.filter(tipo='PJ', cnpj=documento).first()
                if cliente:
                    return JsonResponse({
                        'cliente': {
                            'razao_social': cliente.razao_social,
                            'nome_fantasia': cliente.nome_fantasia,
                            'cnpj': cliente.cnpj
                        }
                    })
            
            return JsonResponse({
                'error': 'Cliente não encontrado'
            }, status=404)
            
        except Exception as e:
            print(f"Erro ao buscar cliente: {str(e)}")  # Log do erro
            return JsonResponse({
                'error': 'Erro ao buscar cliente'
            }, status=500)

class CadastrarVendaView(LoginRequiredMixin, View):
    def post(self, request):
        venda_form = VendaForm(request.POST)
        item_formset = ItemVendaFormSet(request.POST, prefix='itens')

        if venda_form.is_valid() and item_formset.is_valid():
            try:
                with transaction.atomic():
                    venda = venda_form.save(commit=False)
                    venda.cliente = venda_form.cleaned_data['cliente']
                    venda.save()

                    # Salvar itens
                    itens = item_formset.save(commit=False)
                    valor_total = 0
                    for item in itens:
                        item.venda = venda
                        item.valor_unitario = item.produto.preco
                        valor_total += item.subtotal
                        item.save()

                    # Atualizar valor total da venda
                    venda.valor_total = valor_total
                    venda.save()

                return JsonResponse({'success': True})
            except Exception as e:
                return JsonResponse({'success': False, 'error': str(e)}, status=400)
        else:
            errors = {}
            if venda_form.errors:
                errors.update(venda_form.errors)
            if item_formset.errors:
                errors['itens'] = item_formset.errors
            return JsonResponse({'success': False, 'errors': errors}, status=400)
        
class BuscarVendaView(LoginRequiredMixin, View):
    def get(self, request, venda_id):
        try:
            venda = Venda.objects.get(id=venda_id)
            itens = venda.itens.all()  # Acessando os itens da venda
            itens_data = [{
                'produto': item.produto.nome,  # Nome do produto
                'quantidade': item.quantidade,
                'valor_unitario': item.valor_unitario,
                'subtotal': item.subtotal,
            } for item in itens]

            return JsonResponse({
                'success': True,
                'venda': {
                    'id': venda.id,
                    'data_venda': venda.data_venda.strftime('%d/%m/%Y %H:%M'),
                    'valor_total': venda.valor_total,
                    'itens': itens_data,
                }
            })
        except Venda.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'Venda não encontrada'}, status=404)

from .models import Produto

class ListarProdutosView(View):
    def get(self, request):
        produtos = Produto.objects.all().values('id', 'nome', 'preco', 'quantidade')
        return JsonResponse(list(produtos), safe=False)