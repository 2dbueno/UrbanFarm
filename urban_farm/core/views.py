# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Fornecedor, Monitoramento
from .forms import FornecedorForm, EnderecoForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('monitoramento/')
        else:
            error_message = "Usuário ou senha inválidos. Contate seu superior."
            return render(request, 'login.html', {'error_message': error_message})
    return render(request, 'login.html')

@login_required
def monitoramento_view(request):
    return render(request, 'monitoramento.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('core:login')

def monitoramento_view(request):
    # Recupera o primeiro registro de monitoramento no banco de dados
    monitoramento = Monitoramento.objects.first()
    
    # Passa o objeto monitoramento para o template
    return render(request, 'monitoramento.html', {'monitoramento': monitoramento})

def fornecedores_view(request):
    fornecedores = Fornecedor.objects.all()
    form = FornecedorForm()  # Aqui, cria a instância do formulário para ser usada no template
    endereco_form = EnderecoForm()  # Crie uma instância do formulário de endereço
    return render(request, 'fornecedores.html', {'fornecedores': fornecedores, 'form': form, 'endereco_form': endereco_form})

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        fornecedor_form = FornecedorForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if fornecedor_form.is_valid() and endereco_form.is_valid():
            fornecedor = fornecedor_form.save(commit=False)
            endereco = endereco_form.save()
            fornecedor.endereco = endereco
            fornecedor.save()

            # Retorno de sucesso em JSON
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
            # Retorno de erros de validação em JSON
            errors = {**fornecedor_form.errors, **endereco_form.errors}
            return JsonResponse({
                'success': False,
                'errors': errors
            }, status=400)

    return render(request, 'fornecedores.html', {
        'form': FornecedorForm(),
        'endereco_form': EnderecoForm(),
    })