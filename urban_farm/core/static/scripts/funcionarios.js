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

    // Limpa o formulário e redefine a URL para o cadastro de um novo funcionário
    $('#funcionarioForm')[0].reset();
    $('#funcionarioForm').data('url', cadastrar_funcionario_url);
    $('#modal-title').text("Cadastrar Funcionário");

    // Limpa mensagens de erro anteriores
    $('.error-message').remove();
    $('input, select').removeClass('input-error');

    $('#funcionarioForm').find('input, select').prop('disabled', false); // Habilita todos os campos
    $('.submit-btn').text("Cadastrar").show(); // Mostra o botão e define o texto
    $('.edit-buttons').hide(); // Esconde os botões de edição
}

document.getElementsByClassName("close")[0].onclick = function() {
    document.getElementById("modal").style.display = "none";
}

window.onclick = function(event) {
    if (event.target == document.getElementById("modal")) {
        document.getElementById("modal").style.display = "none";
    }
}

// Evento para abrir o modal ao clicar em um funcionário
$('#funcionario-list').on('click', '.funcionario-row', function() {
    var funcionarioId = $(this).data('id'); // Pega o ID do funcionário da linha clicada
    var url = `/funcionarios/${funcionarioId}/`; // Corrigido para usar a rota correta

    // Faz uma requisição AJAX para buscar os dados do funcionário
    $.get(url, function(response) {
        // Limpa mensagens de erro anteriores
        $('.error-message').remove();
        $('input, select').removeClass('input-error');

        // Preenche o formulário com os dados do funcionário
        $('#funcionarioForm').find('[name="nome"]').val(response.funcionario.nome).prop('disabled', true);
        $('#funcionarioForm').find('[name="cpf"]').val(response.funcionario.cpf).prop('disabled', true);
        $('#funcionarioForm').find('[name="cargo"]').val(response.funcionario.cargo).prop('disabled', true);
        $('#funcionarioForm').find('[name="status"]').prop('checked', response.funcionario.status).prop('disabled', true);
        $('#funcionarioForm').find('[name="data_admissao"]').val(response.funcionario.data_admissao).prop('disabled', true);
        $('#funcionarioForm').find('[name="salario"]').val(response.funcionario.salario).prop('disabled', true);

        // Preenche os dados do endereço
        $('#funcionarioForm').find('[name="cep"]').val(response.endereco.cep).prop('disabled', true);
        $('#funcionarioForm').find('[name="endereco"]').val(response.endereco.endereco).prop('disabled', true);
        $('#funcionarioForm').find('[name="complemento"]').val(response.endereco.complemento).prop('disabled', true);
        $('#funcionarioForm').find('[name="cidade"]').val(response.endereco.cidade).prop('disabled', true);
        $('#funcionarioForm').find('[name="estado"]').val(response.endereco.estado).prop('disabled', true);
        $('#funcionarioForm').find('[name="bairro"]').val(response.endereco.bairro).prop('disabled', true);
        $('#funcionarioForm').find('[name="telefone"]').val(response.endereco.telefone).prop('disabled', true);
        $('#funcionarioForm').find('[name="email"]').val(response.endereco.email).prop('disabled', true);

        // Atualiza o título do modal e a URL do formulário para edição
        $('#modal-title').text("Editar Funcionário");
        $('#funcionarioForm').data('url', `${editar_funcionario_url}${funcionarioId}/`);

        // Esconde os botões de "Salvar" e "Cancelar" inicialmente
        $('.edit-buttons').hide(); // Esconde os botões de edição
        $('.submit-btn').text("Editar").show(); // Altera o texto do botão para "Editar"

        // Abre o modal
        document.getElementById("modal").style.display = "block";
    }).fail(function(xhr) {
        console.error('Erro ao buscar funcionário:', xhr);
    });
});

// Evento para o botão de "Editar"
$('.submit-btn').on('click', function(event) {
    event.preventDefault(); // Impede o envio imediato do formulário

    // Habilita todos os campos para edição
    $('#funcionarioForm').find('input, select').prop('disabled', false);
    $('.submit-btn').hide(); // Esconde o botão "Editar"
    $('.edit-buttons').show(); // Mostra os botões "Salvar" e "Cancelar"
});

// Evento para o botão "Salvar"
$('.save-btn').on('click', function(event) {
    event.preventDefault(); // Impede o envio imediato do formulário

    // Confirmação antes de salvar
    if (!confirm("Você tem certeza que deseja salvar as alterações?")) {
        return; // Se o usuário cancelar, sai da função
    }

    // Limpa mensagens de erro anteriores
    $('.error-message').remove();
    $('input, select').removeClass('input-error');

    // Captura a URL correta (cadastrar ou editar)
    var url = $('#funcionarioForm').data('url');

    $.ajax({
        type: 'POST',
        url: url,
        data: $('#funcionarioForm').serialize(),
        success: function(response) {
            // Se for uma edição, atualiza a linha correspondente
            if (response.funcionario_editado) {
                var row = $(`.funcionario-row[data-id="${response.funcionario.id}"]`);
                row.find('td:nth-child(2)').text(response.funcionario.nome);
                row.find('td:nth-child(3)').text(formatarCPF(response.funcionario.cpf));
                row.find('td:nth-child(4)').text(response.funcionario.cargo);
                row.find('td:nth-child(5)').text(response.funcionario.status ? 'ATIVO' : 'INATIVO');
            } else {
                // Se for um novo cadastro, adiciona uma nova linha
                $('#funcionario-list').append(`
                    <tr class="funcionario-row" data-id="${response.funcionario.id}">
                        <td>${response.funcionario.id}</td>
                        <td>${response.funcionario.nome}</td>
                        <td>${formatarCPF(response.funcionario.cpf)}</td>
                        <td>${response.funcionario.cargo}</td>
                        <td class="${response.funcionario.status ? 'ativo' : 'inativo'}">${response.funcionario.status ? 'ATIVO' : 'INATIVO'}</td>
                        <td>
                            ${response.user_is_superuser ? `<button class="edit-btn" aria-label="Editar funcionário" data-id="${response.funcionario.id}">Editar</button>` : '<span title="Você não tem permissão para editar este funcionário">🔒</span>'}
                        </td>
                    </tr>
                `);
            }

            // Fecha o modal
            document.getElementById("modal").style.display = "none";

            // Reseta o formulário
            $('#funcionarioForm')[0].reset();

            // Atualiza a página
            location.reload(); // Recarrega a página
        },
        error: function(xhr) {
            // Trata os erros de validação
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

// Evento para o botão "Cancelar"
$('.cancel-btn').on('click', function() {
    $('#funcionarioForm')[0].reset(); // Reseta o formulário
    document.getElementById("modal").style.display = "none"; // Fecha o modal
    $('.edit-buttons').hide(); // Esconde os botões de "Salvar" e "Cancelar"
    $('.submit-btn').show(); // Mostra o botão "Editar" novamente
});
