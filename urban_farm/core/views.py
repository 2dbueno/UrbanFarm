# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Fornecedor, Monitoramento, Planta, Funcionario, Cliente, Venda, ItemVenda
from .forms import FornecedorForm, EnderecoForm, FuncionarioForm, ClienteForm, VendaForm, ItemVendaForm

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
        # Obtém o primeiro objeto de monitoramento
        monitoramento = Monitoramento.objects.first()
        
        # Conta o número total de vendas
        total_vendas = Venda.objects.count()

        # Passa o monitoramento e total de vendas para o template
        return render(request, self.template_name, {'monitoramento': monitoramento, 'total_vendas': total_vendas})
    
# View para realizar logout do usuário.
class LogoutView(View):
    def post(self, request):
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

        # Cria um dicionário para o cliente
        cliente_data = {
            'tipo': cliente.tipo,
            'status': cliente.status,
        }

        # Adiciona campos específicos de PF ou PJ
        if cliente.tipo == 'PF':
            cliente_data['cpf'] = cliente.cpf
            cliente_data['nome'] = cliente.nome
        elif cliente.tipo == 'PJ':
            cliente_data['cnpj'] = cliente.cnpj
            cliente_data['razao_social'] = cliente.razao_social
            cliente_data['nome_fantasia'] = cliente.nome_fantasia

        return JsonResponse({
            'cliente': cliente_data,
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
        
import logging
# Configuração do sistema de logging:
# Define o nível mínimo de severidade das mensagens a serem registradas como INFO,
# o que significa que mensagens de nível INFO, WARNING, ERROR e CRITICAL serão capturadas.
# As mensagens incluirá a data e hora do log, o nível de severidade(forma de classificar a importância/gravidade das mensagens)
# e a mensagem em si.

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
class VendasView(View):
    template_name = 'vendas.html'

    def get(self, request):
        
        vendas = Venda.objects.all()
        form = VendaForm()
        clientes = Cliente.objects.all()
        return render(request, self.template_name, {
            'vendas': vendas,
            'form': form,
            'clientes': clientes,
        })


class CadastrarVendaView(View):
    def post(self, request):
        venda_form = VendaForm(request.POST)

        if venda_form.is_valid():
            venda = venda_form.save()

            # Log dos dados da venda
            logging.info("Venda cadastrada com sucesso:")
            logging.info(f"ID da Venda: {venda.id}")
            logging.info(f"Cliente: {venda.cliente.nome}")
            logging.info(f"Preço Total: {venda.preco_total}")
            logging.info(f"Data da Venda: {venda.data_venda}")

            # Processa os itens de venda
            itens_da_venda = []
            item_count = int(request.POST.get('item_count', 0))
            logging.info(f"Quantidade de itens a serem processados: {item_count}")

            for i in range(item_count):
                item_nome = request.POST.get(f'itens-{i}-item')
                item_quantidade = request.POST.get(f'itens-{i}-quantidade')
                item_valor_unitario = request.POST.get(f'itens-{i}-valor_unitario')

                # Log dos dados do item
                logging.info(f"Processando item {i}: Nome: {item_nome}, Quantidade: {item_quantidade}, Valor Unitário: {item_valor_unitario}")

                # Verifica se os campos não estão vazios ou None
                if item_nome and item_quantidade and item_valor_unitario:
                    try:
                        item_quantidade = int(item_quantidade)
                        item_valor_unitario = float(item_valor_unitario)
                    except (ValueError, TypeError):
                        logging.warning(f"Erro ao converter item: {item_nome}, quantidade: {item_quantidade}, valor unitário: {item_valor_unitario}")
                        continue  # Ignora este item se houver erro de conversão

                    item_form = ItemVendaForm({
                        'item': item_nome,
                        'quantidade': item_quantidade,
                        'valor_unitario': item_valor_unitario,
                    })

                    if item_form.is_valid():
                        item = item_form.save(commit=False)
                        item.venda = venda  # Associa o item à venda
                        item.save()

                        # Log dos dados do item
                        logging.info("Item de venda cadastrado:")
                        logging.info(f" - Nome do Item: {item.item}")
                        logging.info(f" - Quantidade: {item.quantidade}")
                        logging.info(f" - Valor Unitário: {item.valor_unitario}")
                        itens_da_venda.append(item)
                    else:
                        logging.warning(f"Erro ao cadastrar item: {item_form.errors}")
                else:
                    logging.warning(f"Dados do item {i} estão incompletos: Nome: {item_nome}, Quantidade: {item_quantidade}, Valor Unitário: {item_valor_unitario}")

            if not itens_da_venda:
                logging.warning("Nenhum item de venda foi cadastrado. Verifique os dados do formulário e do banco de dados.")

            # Retorne um JSON de sucesso
            return JsonResponse({'success': True, 'venda_id': venda.id})

        # Se o formulário não for válido, retorne os erros como JSON
        return JsonResponse({'success': False, 'errors': venda_form.errors}, status=400)


class EditarVendaView(View):
    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, id=venda_id)
        form = VendaForm(instance=venda)
        itens = ItemVenda.objects.filter(venda=venda)  # Obtém os itens associados à venda
        return render(request, 'vendas.html', {
            'form': form,
            'venda': venda,
            'itens': itens,  # Passa os itens para o template
        })

    def post(self, request, venda_id):
        venda = get_object_or_404(Venda, id=venda_id)
        form = VendaForm(request.POST, instance=venda)

        if form.is_valid():
            form.save()  # Salva a venda

            # Atualiza os itens de venda
            item_count = int(request.POST.get('item_count', 0))
            ItemVenda.objects.filter(venda=venda).delete()  # Remove itens existentes antes de atualizar

            for i in range(item_count):
                item_nome = request.POST.get(f'itens-{i}-item')
                item_quantidade = request.POST.get(f'itens-{i}-quantidade')
                item_valor_unitario = request.POST.get(f'itens-{i}-valor_unitario')

                if item_nome and item_quantidade and item_valor_unitario:
                    item_form = ItemVendaForm({
                        'item': item_nome,
                        'quantidade': item_quantidade,
                        'valor_unitario': item_valor_unitario,
                    })

                    if item_form.is_valid():
                        item = item_form.save(commit=False)
                        item.venda = venda  # Associa o item à venda
                        item.save()  # Salva o item

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)

class BuscarVendaView(View):
    def get(self, request, venda_id):
        venda = get_object_or_404(Venda, id=venda_id)
        itens = ItemVenda.objects.filter(venda=venda)
        
        response_data = {
            'venda': {
                'id': venda.id,
                'cliente_id': venda.cliente.id,  # Inclua o ID do cliente
                'cliente': venda.cliente.nome,
                'preco_total': venda.preco_total,
                'data_venda': venda.data_venda,
            },
            'itens': [
                {
                    'item': item.item,
                    'quantidade': item.quantidade,
                    'valor_unitario': item.valor_unitario,
                } for item in itens
            ]
        }
        return JsonResponse(response_data)