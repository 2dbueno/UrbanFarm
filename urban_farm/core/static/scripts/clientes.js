// Função para formatar o CPF
function formatarCPF(cpf) {
    if (cpf.length === 11) {
        return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9)}`;
    }
    return cpf; }

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
    confirmModal.style.display = 'block';
}

// Evento para o botão de "Sim" no popup de confirmação
confirmYesBtn.addEventListener('click', function() {
    $('#clienteForm').submit();
    confirmModal.style.display = 'none';
    location.reload();
});

// Evento para o botão de "Não" no popup de confirmação
confirmNoBtn.addEventListener('click', function() {
    confirmModal.style.display = 'none';
});

$(document).ready(function() {
    // Evento para abrir o modal ao clicar em um cliente
    $('.cliente-row').on('click', function() {
        var clienteId = $(this).data('id');
        var url = buscar_cliente_url + clienteId + '/';

        $.get(url, function(response) {
            // Limpa mensagens de erro anteriores
            $('.error-message').remove();
            $('input, select').removeClass('input-error');

            // Preenche o formulário com os dados do cliente
            $('#clienteForm').find('[name="cpf"]').val(response.cliente.cpf);
            $('#clienteForm').find('[name="nome"]').val(response.cliente.nome);
            $('#clienteForm').find('[name="status"]').prop('checked', response.cliente.status);

            // Preenche os dados do endereço
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
            $('.edit-buttons').show();
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

        $('.error-message').remove();
        $('input, select').removeClass('input-error');

        var url = $(this).data('url');

        $.ajax({
            type: 'POST',
            url: url,
            data: $(this).serialize(),
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