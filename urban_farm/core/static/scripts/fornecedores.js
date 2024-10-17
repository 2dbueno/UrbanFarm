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
    $('#fornecedorForm').on('submit', function(event) {
        event.preventDefault();  // Previne o comportamento padrão de submissão

        // Limpa mensagens de erro anteriores
        $('.error-message').remove();
        $('input, select').removeClass('input-error');

        $.ajax({
            type: 'POST',
            url: cadastrar_fornecedor_url,
            data: $(this).serialize(),
            success: function(response) {
                // Adiciona o novo fornecedor na tabela
                $('#fornecedor-list').append(`<tr>
                    <td>${response.fornecedor.id}</td>
                    <td>${response.fornecedor.nome_fantasia}</td>
                    <td>${formatarCNPJ(response.fornecedor.cnpj)}</td>  // Formatação do CNPJ aqui
                    <td ${response.fornecedor.status}</td>
                </tr>`);
                // Fecha o modal
                document.getElementById("modal").style.display = "none";
                location.reload() // Atualiza a pagina para atualizar o status do fornecedor
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
