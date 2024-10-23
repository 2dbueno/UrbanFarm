# core/views.py

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views import View
from .models import Fornecedor, Monitoramento, Planta
from .forms import FornecedorForm, EnderecoForm

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
        # Autentica o usuário com base no nome de usuário e senha fornecidos.
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Faz o login do usuário.
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
            fornecedor_form.save()  # Salva as alterações do fornecedor.
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