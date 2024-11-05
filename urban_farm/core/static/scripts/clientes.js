// Função para formatar o CPF
function formatarCPF(cpf) {
    if (cpf.length === 11) {
        return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9)}`;
    }
    return cpf;
}

// Função para formatar o CNPJ
function formatarCNPJ(cnpj) {
    if (cnpj.length === 14) {
        return `${cnpj.slice(0, 2)}.${cnpj.slice(2, 5)}.${cnpj.slice(5, 8)}/${cnpj.slice(8, 12)}-${cnpj.slice(12)}`;
    }
    return cnpj;
}

// Função para validar campos obrigatórios baseado no tipo
function validarCamposObrigatorios() {
    const tipo = $('#tipo').val();
    let isValid = true;
    $('.error-message').remove();

    if (!tipo) {
        $('#tipo').addClass('input-error');
        $('#tipo').after('<div class="error-message">Selecione o tipo de cliente</div>');
        isValid = false;
    }

    if (tipo === 'PF') {
        if (!$('#cpf').val()) {
            $('#cpf').addClass('input-error');
            $('#cpf').after('<div class="error-message">CPF é obrigatório</div>');
            isValid = false;
        }
        if (!$('#nome').val()) {
            $('#nome').addClass('input-error');
            $('#nome').after('<div class="error-message">Nome é obrigatório</div>');
            isValid = false;
        }
    } else if (tipo === 'PJ') {
        if (!$('#cnpj').val()) {
            $('#cnpj').addClass('input-error');
            $('#cnpj').after('<div class="error-message">CNPJ é obrigatório</div>');
            isValid = false;
        }
        if (!$('#razao_social').val()) {
            $('#razao_social').addClass('input-error');
            $('#razao_social').after('<div class="error-message">Razão Social é obrigatória</div>');
            isValid = false;
        }
    }

    return isValid;
}

// Script para abrir e fechar o popup
document.getElementById("openModal").onclick = function() {
    document.getElementById("modal").style.display = "block";

    // Limpa o formulário e redefine a URL para o cadastro
    $('#clienteForm')[0].reset();
    $('#clienteForm').data('url', cadastrar_cliente_url);
    $('#modal-title').text("Cadastrar Cliente");

    // Limpa mensagens de erro anteriores
    $('.error-message').remove();
    $('input, select').removeClass('input-error');

    // Reseta e esconde os campos específicos
    $('.pessoa-fisica, .pessoa-juridica').hide();
    $('#tipo').val('');

    $('#clienteForm').find('input, select').prop('disabled', false);
    $('.submit-btn').text("Cadastrar").show();
    $('.edit-buttons').hide();
}

document.getElementsByClassName("close")[0].onclick = function() {
    document.getElementById("modal").style.display = "none";
}

window.onclick = function(event) {
    if (event.target == document.getElementById("modal")) {
        document.getElementById("modal").style.display = "none";
    }
}

// Selecionar os elementos do modal de confirmação
var confirmModal = document.getElementById('confirmModal');
var confirmYesBtn = document.querySelector('.confirm-yes-btn');
var confirmNoBtn = document.querySelector('.confirm-no-btn');

// Função para abrir o modal de confirmação
function abrirConfirmacao() {
    if (validarCamposObrigatorios()) {
        confirmModal.style.display = 'block';
    }
}

// Evento para o botão de "Sim" no popup de confirmação
confirmYesBtn.addEventListener('click', function() {
    $('#clienteForm').submit();
    confirmModal.style.display = 'none';
});

// Evento para o botão de "Não" no popup de confirmação
confirmNoBtn.addEventListener('click', function() {
    confirmModal.style.display = 'none';
});

$(document).ready(function() {
    // Aplicar máscaras aos campos
    $('#cpf').mask('000.000.000-00');
    $('#cnpj').mask('00.000.000/0000-00');
    $('#telefone').mask('(00) 00000-0000');
    $('#cep').mask('00000-000');

    // Evento para alternar entre PF e PJ
    $('#tipo').on('change', function() {
        const tipo = $(this).val();
        $('.pessoa-fisica, .pessoa-juridica').hide();
        $('input, select').removeClass('input-error');
        $('.error-message').remove();

        if (tipo === 'PF') {
            $('.pessoa-fisica').show();
            $('#cnpj, #razao_social, #nome_fantasia').val('');
        } else if (tipo === 'PJ') {
            $('.pessoa-juridica').show();
            $('#cpf, #nome').val('');
        }
    });

    // Evento para abrir o modal ao clicar em um cliente
    $('.cliente-row').on('click', function() {
        var clienteId = $(this).data('id');
        var url = buscar_cliente_url + clienteId + '/';

        $.get(url, function(response) {
            console.log(response)
            // Limpa mensagens de erro anteriores
            $('.error-message').remove();
            $('input, select').removeClass('input-error');

            // Define o tipo e mostra os campos apropriados
            $('#tipo').val(response.cliente.tipo);
            if (response.cliente.tipo === 'PF') {
                $('.pessoa-fisica').show();
                $('.pessoa-juridica').hide();
                $('#cpf').val(response.cliente.cpf);
                $('#nome').val(response.cliente.nome);
            } else {
                $('.pessoa-juridica').show();
                $('.pessoa-fisica').hide();
                $('#cnpj').val(response.cliente.cnpj);
                $('#razao_social').val(response.cliente.razao_social);
                $('#nome_fantasia').val(response.cliente.nome_fantasia);
            }

            // Atualiza o status do cliente
            if (response.cliente.status) {
                $('#status').prop('checked', true);
            } else {
                $('#status').prop('checked', false);
            }

            // Preenche os dados de endereço
            $('#clienteForm').find('[name="cep"]').val(response.endereco.cep);
            $('#clienteForm').find('[name="endereco"]').val(response.endereco.endereco);
            $('#clienteForm').find('[name="complemento"]').val(response.endereco.complemento);
            $('#clienteForm').find('[name="cidade"]').val(response.endereco.cidade);
            $('#clienteForm').find('[name="estado"]').val(response.endereco.estado);
            $('#clienteForm').find('[name="bairro"]').val(response.endereco.bairro);
            $('#clienteForm').find('[name="telefone"]').val(response.endereco.telefone);
            $('#clienteForm').find('[name="email"]').val(response.endereco.email);

            // Atualiza o título do modal e a URL do formulário
            $('#modal-title').text("Editar Cliente");
            $('#clienteForm').data('url', `${editar_cliente_url}${clienteId}/`);

            // Desabilita os campos inicialmente
            $('#clienteForm').find('input, select').prop('disabled', true);
            $('.submit-btn').text("Editar").show();
            $('.edit-buttons').hide();

            document.getElementById("modal").style.display = "block";
        });
    });

    // Evento para o botão principal (Cadastrar/Editar)
    $('.submit-btn').on('click', function(event) {
        event.preventDefault();
        if ($(this).text() === "Cadastrar") {
            abrirConfirmacao();
        } else {
            $('#clienteForm').find('input, select').prop('disabled', false);
            $(this).hide();
            $('.edit-buttons').show ();
        }
    });

    // Evento para o botão "Salvar"
    $('.save-btn').on('click', function(event) {
        event.preventDefault();
        abrirConfirmacao();
    });

    // Evento para o botão "Cancelar"
    $('.cancel-btn').on('click', function() {
        $('#clienteForm')[0].reset();
        document.getElementById("modal").style.display = "none";
        $('.edit-buttons').hide();
        $('.submit-btn').show();
    });

    // Manipulação do formulário
    $('#clienteForm').on('submit', function(event) {
        event.preventDefault();

        var url = $(this).data('url');
        var formData = $(this).serialize();

        $.ajax({
            type: 'POST',
            url: url,
            data: formData,
            success: function(response) {
                if (response.success) {
                    location.reload();
                }
            },
            error: function(xhr) {
                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    $.each(xhr.responseJSON.errors, function(key, value) {
                        var inputField = $(`[name="${key}"]`);
                        inputField.addClass('input-error');
                        inputField.after(`<div class="error-message">${value[0]}</div>`);
                    });
                }
            }
        });
    });
});