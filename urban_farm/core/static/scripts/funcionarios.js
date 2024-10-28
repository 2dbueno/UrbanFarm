// Função para formatar o CPF
function formatarCPF(cpf) {
    if (cpf.length === 11) {
        return `${cpf.slice(0, 3)}.${cpf.slice(3, 6)}.${cpf.slice(6, 9)}-${cpf.slice(9)}`;
    }
    return cpf;
}

// Script para abrir e fechar o popup
document.getElementById("openModal").onclick = function() {
    document.getElementById("modal").style.display = "block";

    // Limpa o formulário e redefine a URL para o cadastro
    $('#funcionarioForm')[0].reset();
    $('#funcionarioForm').data('url', cadastrar_funcionario_url);
    $('#modal-title').text("Cadastrar Funcionário");

    // Limpa mensagens de erro anteriores
    $('.error-message').remove();
    $('input, select').removeClass('input-error');

    $('#funcionarioForm').find('input, select').prop('disabled', false);
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
    $('#funcionarioForm').submit();
    confirmModal.style.display = 'none';
    location.reload();
});

// Evento para o botão de "Não" no popup de confirmação
confirmNoBtn.addEventListener('click', function() {
    confirmModal.style.display = 'none';
});

$(document).ready(function() {
    // Evento para abrir o modal ao clicar em um funcionário
    $('.funcionario-row').on('click', function() {
        var funcionarioId = $(this).data('id');
        var url = buscar_funcionario_url + funcionarioId + '/';

        $.get(url, function(response) {
            // Limpa mensagens de erro anteriores
            $('.error-message').remove();
            $('input, select').removeClass('input-error');

            // Preenche o formulário com os dados do funcionário
            $('#funcionarioForm').find('[name="cpf"]').val(response.funcionario.cpf);
            $('#funcionarioForm').find('[name="nome"]').val(response.funcionario.nome);
            $('#funcionarioForm').find('[name="cargo"]').val(response.funcionario.cargo);
            $('#funcionarioForm').find('[name="data_admissao"]').val(response.funcionario.data_admissao);
            $('#funcionarioForm').find('[name="salario"]').val(response.funcionario.salario);
            $('#funcionarioForm').find('[name="status"]').prop('checked', response.funcionario.status);

            // Preenche os dados do endereço
            $('#funcionarioForm').find('[name="cep"]').val(response.endereco.cep);
            $('#funcionarioForm').find('[name="endereco"]').val(response.endereco.endereco);
            $('#funcionarioForm').find('[name="complemento"]').val(response.endereco.complemento);
            $('#funcionarioForm').find('[name="cidade"]').val(response.endereco.cidade);
            $('#funcionarioForm').find('[name="estado"]').val(response.endereco.estado);
            $('#funcionarioForm').find('[name="bairro"]').val(response.endereco.bairro);
            $('#funcionarioForm').find('[name="telefone"]').val(response.endereco.telefone);
            $('#funcionarioForm').find('[name="email"]').val(response.endereco.email);

            // Atualiza o título do modal e a URL do formulário
            $('#modal-title').text("Editar Funcionário");
            $('#funcionarioForm').data('url', `${editar_funcionario_url}${funcionarioId}/`);

            // Desabilita os campos inicialmente
            $('#funcionarioForm').find('input, select').prop('disabled', true);
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
            $('#funcionarioForm').find('input, select').prop('disabled', false);
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
        $('#funcionarioForm')[0].reset();
        document.getElementById("modal").style.display = "none";
        $('.edit-buttons').hide();
        $('.submit-btn').show();
    });

    // Manipulação do formulário
    $('#funcionarioForm').on('submit', function(event) {
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