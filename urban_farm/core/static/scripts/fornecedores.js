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

$(document).ready(function() {
    // Evento para carregar dados no modal para edição ao clicar em qualquer linha da tabela
    $('.fornecedor-row').on('click', function() {
        var fornecedorId = $(this).data('id'); // Pega o ID do fornecedor da linha clicada
        var url = `/buscar_fornecedor/${fornecedorId}/`;

        // Faz uma requisição AJAX para buscar os dados do fornecedor
        $.get(url, function(response) {
            // Preenche o formulário com os dados do fornecedor
            $('#fornecedorForm').find('[name="cnpj"]').val(response.fornecedor.cnpj);
            $('#fornecedorForm').find('[name="status"]').prop('checked', response.fornecedor.status);
            $('#fornecedorForm').find('[name="razao_social"]').val(response.fornecedor.razao_social);
            $('#fornecedorForm').find('[name="nome_fantasia"]').val(response.fornecedor.nome_fantasia);
            $('#fornecedorForm').find('[name="nome_representante"]').val(response.fornecedor.nome_representante);
            $('#fornecedorForm').find('[name="cep"]').val(response.endereco.cep);
            $('#fornecedorForm').find('[name="endereco"]').val(response.endereco.endereco);
            $('#fornecedorForm').find('[name="complemento"]').val(response.endereco.complemento);
            $('#fornecedorForm').find('[name="cidade"]').val(response.endereco.cidade);
            $('#fornecedorForm').find('[name="estado"]').val(response.endereco.estado);
            $('#fornecedorForm').find('[name="bairro"]').val(response.endereco.bairro);
            $('#fornecedorForm').find('[name="telefone"]').val(response.endereco.telefone);
            $('#fornecedorForm').find('[name="email"]').val(response.endereco.email);

            $('#fornecedorForm').find('[name="id"]').val(response.fornecedor.id);

            // Atualiza o título do modal e a URL do formulário para edição
            $('#modal-title').text("Editar Fornecedor");
            $('#fornecedorForm').data('url', `/editar_fornecedor/${fornecedorId}/`);
            
            // Abre o modal
            document.getElementById("modal").style.display = "block";
        }).fail(function(xhr) {
            console.error('Erro ao buscar fornecedor:', xhr);
        });
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
                    $(`#fornecedor-${response.fornecedor.id}`).html(`
                        <td>${response.fornecedor.id}</td>
                        <td>${response.fornecedor.nome_fantasia}</td>
                        <td>${formatarCNPJ(response.fornecedor.cnpj)}</td>
                        <td>${response.fornecedor.status}</td>
                    `);
                } else {
                    // Adiciona o novo fornecedor na tabela (cadastro)
                    $('#fornecedor-list').append(`<tr id="fornecedor-${response.fornecedor.id}">
                        <td>${response.fornecedor.id}</td>
                        <td>${response.fornecedor.nome_fantasia}</td>
                        <td>${formatarCNPJ(response.fornecedor.cnpj)}</td>  // Formatação do CNPJ aqui
                        <td>${response.fornecedor.status}</td>
                    </tr>`);
                }

                // Fecha o modal
                document.getElementById("modal").style.display = "none";
                location.reload(); // Atualiza a página para refletir as mudanças
            },
            error: function(xhr) {
                if (xhr.status === 400) { // Se houver um erro 400 (Bad Request)
                    const errors = xhr.responseJSON.errors;
                    
                    // Itera sobre os erros e exibe no campo correto
                    $.each(errors, function(field, messages) {
                        const input = $(`[name=${field}]`);
                        input.addClass('input-error');  // Adiciona uma classe de erro ao campo
                        input.after(`<span class="error-message">${messages[0]}</span>`);  // Mostra a mensagem de erro
                    });
                } else {
                    // Se houver outro erro, exiba uma mensagem genérica no console
                    console.error('Erro desconhecido no cadastro:', xhr);
                }
            }
        });
    });
});
