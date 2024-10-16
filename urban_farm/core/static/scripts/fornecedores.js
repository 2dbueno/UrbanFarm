// Função para formatar o CNPJ
function formatarCNPJ(cnpj) {
    if (cnpj.length === 14) {
        return `${cnpj.slice(0, 2)}.${cnpj.slice(2, 5)}.${cnpj.slice(5, 8)}/${cnpj.slice(8, 12)}-${cnpj.slice(12)}`;
    }
    return cnpj; // Retorna o CNPJ sem formatação se não tiver 14 dígitos
}

// Script para abrir e fechar o popup
document.getElementById("openModal").onclick = function() {
    document.getElementById("modal").style.display = "block";

    // Limpa o formulário e redefine a URL para o cadastro de um novo fornecedor
    $('#fornecedorForm')[0].reset();
    $('#fornecedorForm').data('url', cadastrar_fornecedor_url);
    $('#modal-title').text("Cadastrar Fornecedor");
}

document.getElementsByClassName("close")[0].onclick = function() {
    document.getElementById("modal").style.display = "none";
}

window.onclick = function(event) {
    if (event.target == document.getElementById("modal")) {
        document.getElementById("modal").style.display = "none";
    }
}

// Variável para armazenar a URL de cadastro de fornecedor
var cadastrar_fornecedor_url = cadastrar_fornecedor_url;

// Script para abrir e fechar o popup
document.getElementById("openModal").onclick = function() {
    document.getElementById("modal").style.display = "block";

    // Limpa o formulário e redefine a URL para o cadastro de um novo fornecedor
    $('#fornecedorForm')[0].reset();
    $('#fornecedorForm').data('url', cadastrar_fornecedor_url);
    $('#modal-title').text("Cadastrar Fornecedor");

    // Certifique-se de que todos os campos estão habilitados para cadastro
    $('#fornecedorForm').find('input, select').prop('disabled', false); // Habilita todos os campos
    $('.submit-btn').text("Cadastrar"); // Define o texto do botão como "Cadastrar"
}

// Variável para armazenar a URL de cadastro de fornecedor
var cadastrar_fornecedor_url = cadastrar_fornecedor_url;

$(document).ready(function() {
    // Evento para abrir o modal ao clicar em um fornecedor
    $('.fornecedor-row').on('click', function() {
        var fornecedorId = $(this).data('id'); // Pega o ID do fornecedor da linha clicada
        var url = `/buscar_fornecedor/${fornecedorId}/`;
    
        // Faz uma requisição AJAX para buscar os dados do fornecedor
        $.get(url, function(response) {
            // Preenche o formulário com os dados do fornecedor
            $('#fornecedorForm').find('[name="cnpj"]').val(response.fornecedor.cnpj).prop('disabled', true);
            $('#fornecedorForm').find('[name="status"]').prop('checked', response.fornecedor.status).prop('disabled', true);
            $('#fornecedorForm').find('[name="razao_social"]').val(response.fornecedor.razao_social).prop('disabled', true);
            $('#fornecedorForm').find('[name="nome_fantasia"]').val(response.fornecedor.nome_fantasia).prop('disabled', true);
            $('#fornecedorForm').find('[name="nome_representante"]').val(response.fornecedor.nome_representante).prop('disabled', true);
            $('#fornecedorForm').find('[name="cep"]').val(response.endereco.cep).prop('disabled', true);
            $('#fornecedorForm').find('[name="endereco"]').val(response.endereco.endereco).prop('disabled', true);
            $('#fornecedorForm').find('[name="complemento"]').val(response.endereco.complemento).prop('disabled', true);
            $('#fornecedorForm').find('[name="cidade"]').val(response.endereco.cidade).prop('disabled', true);
            $('#fornecedorForm').find('[name="estado"]').val(response.endereco.estado).prop('disabled', true);
            $('#fornecedorForm').find('[name="bairro"]').val(response.endereco.bairro).prop('disabled', true);
            $('#fornecedorForm').find('[name="telefone"]').val(response.endereco.telefone).prop('disabled', true);
            $('#fornecedorForm').find('[name="email"]').val(response.endereco.email).prop('disabled', true);
    
            $('#fornecedorForm').find('[name="id"]').val(response.fornecedor.id);
    
            // Atualiza o título do modal e a URL do formulário para edição
            $('#modal-title').text("Editar Fornecedor");
            $('#fornecedorForm').data('url', `/editar_fornecedor/${fornecedorId}/`);
    
            // Altera o texto do botão de submissão para "Editar"
            $('.submit-btn').text("Editar");
    
            // Abre o modal
            document.getElementById("modal").style.display = "block";
        }).fail(function(xhr) {
            console.error('Erro ao buscar fornecedor:', xhr);
        });
    });
    
    // Evento para habilitar os campos ao clicar no botão "Editar"
    $('.submit-btn').on('click', function(event) {
        event.preventDefault(); // Previne a submissão do formulário

        // Habilita todos os campos do formulário, incluindo status
        $('#fornecedorForm').find('input, select').prop('disabled', false);
        $('#fornecedorForm').find('[name="status"]').prop('disabled', false);

        // Esconde o botão "Editar" e mostra "Salvar" e "Cancelar"
        $(this).hide();
        $('.edit-buttons').show();
    });

    // Evento para o botão "Salvar"
    $('.save-btn').on('click', function() {
        $('#fornecedorForm').submit(); // Submete o formulário
    });

    // Evento para o botão "Cancelar"
    $('.cancel-btn').on('click', function() {
        $('#fornecedorForm')[0].reset(); // Reseta o formulário
        document.getElementById("modal").style.display = "none"; // Fecha o modal
        $('.edit-buttons').hide(); // Esconde os botões de "Salvar" e "Cancelar"
        $('.submit-btn').show(); // Mostra o botão "Editar" novamente
    });

    $('#fornecedorForm').on('submit', function(event) {
        event.preventDefault();  // Previne o comportamento padrão de submissão

        // Limpa mensagens de erro anteriores
        $('.error-message').remove();
        $('input, select').removeClass('input-error');

        // Captura a URL correta (cadastrar ou editar)
        var url = $(this).data('url');

        $.ajax({
            type: 'POST',
            url: url,
            data: $(this).serialize(),
            success: function(response) {
                // Se for uma edição, atualiza a linha da tabela correspondente
                if (response.fornecedor_editado) {
                    var row = $(`.fornecedor-row[data-id="${response.fornecedor.id}"]`);
                    row.find('td:nth-child(2)').text(response.fornecedor.nome_fantasia);
                    row.find('td:nth-child(3)').text(response.fornecedor.cnpj | format_cnpj);
                    row.find('td:nth-child(4)').text(response.fornecedor.status ? 'ATIVO' : 'INATIVO');
                } else {
                    // Se for um novo cadastro, adiciona uma nova linha
                    $('#fornecedor-list').append(`
                        <tr class="fornecedor-row" data-id="${response.fornecedor.id}">
                            <td>${response.fornecedor.id}</td>
                            <td>${response.fornecedor.nome_fantasia}</td>
                            <td>${response.fornecedor.cnpj | format_cnpj}</td>
                            <td class="${response.fornecedor.status ? 'ativo' : 'inativo'}">${response.fornecedor.status ? 'ATIVO' : 'INATIVO'}</td>
                        </tr>
                    `);
                }

                // Fecha o modal e reseta o formulário
                $('#fornecedorForm')[0].reset();
                document.getElementById("modal").style.display = "none";
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
});
