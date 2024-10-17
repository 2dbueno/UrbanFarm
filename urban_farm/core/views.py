# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from .models import Fornecedor, Monitoramento
from .forms import FornecedorForm, EnderecoForm

# Classe de login
class LoginView(View):
    template_name = 'login.html'

    def get(self, request):
        # Verifica se o usuário já está logado
        if request.user.is_authenticated:
            # Redireciona para a página inicial
            return redirect('monitoramento/')
        return render(request, self.template_name)
    
    def post(self, request):
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('monitoramento/')
        else:
            error_message = "Usuário ou senha inválidos. Contate seu superior."
            return render(request, self.template_name, {'error_message': error_message})
        
# Classe para monitoramento
class MonitoramentoView(LoginRequiredMixin, View):
    template_name = 'monitoramento.html'

    def get(self, request):
        monitoramento = Monitoramento.objects.first()
        return render(request, self.template_name, {'monitoramento': monitoramento})

# Classe para logout
class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('core:login')

# Classe para exibição dos fornecedores
class FornecedoresView(LoginRequiredMixin, View):
    template_name = 'fornecedores.html'

    def get(self, request):
        fornecedores = Fornecedor.objects.all()
        form = FornecedorForm()
        endereco_form = EnderecoForm()
        return render(request, self.template_name, {
            'fornecedores': fornecedores, 
            'form': form, 
            'endereco_form': endereco_form
        })

# Classe para cadastrar fornecedor
class CadastrarFornecedorView(View):

    def post(self, request):
        fornecedor_form = FornecedorForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if fornecedor_form.is_valid() and endereco_form.is_valid():
            fornecedor = fornecedor_form.save(commit=False)
            endereco = endereco_form.save()
            fornecedor.endereco = endereco
            fornecedor.save()

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
            errors = {**fornecedor_form.errors, **endereco_form.errors}
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)

    def get(self, request):
        return render(request, 'fornecedores.html', {
            'form': FornecedorForm(),
            'endereco_form': EnderecoForm(),
        })
