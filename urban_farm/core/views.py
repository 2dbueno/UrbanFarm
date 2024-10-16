# core/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Fornecedor
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

def fornecedores_view(request):
    fornecedores = Fornecedor.objects.all()
    form = FornecedorForm()  # Aqui, cria a instância do formulário para ser usada no template
    endereco_form = EnderecoForm()  # Crie uma instância do formulário de endereço
    return render(request, 'fornecedores.html', {'fornecedores': fornecedores, 'form': form, 'endereco_form': endereco_form})

def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        endereco_form = EnderecoForm(request.POST)

        if form.is_valid() and endereco_form.is_valid():
            # Primeiro salvamos o endereço
            endereco = endereco_form.save()

            # Em seguida, associamos o endereço ao fornecedor e salvamos o fornecedor
            fornecedor = form.save(commit=False)
            fornecedor.endereco = endereco
            fornecedor.save()

            # Retorna uma resposta JSON com os dados do fornecedor cadastrado
            return JsonResponse({'fornecedor': {'id': fornecedor.id, 'nome_fantasia': fornecedor.nome_fantasia, 'cnpj': fornecedor.cnpj}})
    else:
        form = FornecedorForm()
        endereco_form = EnderecoForm()

    return render(request, 'fornecedores.html', {'form': form, 'endereco_form': endereco_form})