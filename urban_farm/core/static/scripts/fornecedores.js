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

// AJAX para enviar o formulário
$(document).ready(function() {
    $('#fornecedorForm').on('submit', function(event) {
        event.preventDefault();  // Previne o comportamento padrão de submissão

        $.ajax({
            type: 'POST',
            url: cadastrar_fornecedor_url,
            data: $(this).serialize(),
            success: function(response) {
                // Adiciona o novo fornecedor na tabela
                $('#fornecedor-list').append(`<tr>
                    <td>${response.fornecedor.id}</td>
                    <td>${response.fornecedor.nome_fantasia}</td>
                    <td>${response.fornecedor.cnpj}</td>
                    <td class="ativo">ATIVO</td>
                </tr>`);

                // Fecha o modal
                document.getElementById("modal").style.display = "none";
            },
            error: function(xhr) {
                // Lidar com erros do formulário
                const errors = xhr.responseJSON.errors;
                alert('Erro ao cadastrar fornecedor: ' + JSON.stringify(errors));
            }
        });
    });
});