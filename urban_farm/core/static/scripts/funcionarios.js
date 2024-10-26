// core/static/scripts/funcionarios.js

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

    // Limpa o formulário e mensagens de erro
    $('#funcionarioForm')[0].reset();
    $('.error-message').remove();
    $('input, select').removeClass('input-error');

    // Habilita campos e configura botões
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

$(document).ready(function() {
    $('#funcionarioForm').on('submit', function(e) {
        e.preventDefault();
        
        // Adiciona o status do checkbox aos dados do formulário
        var formData = new FormData(this);
        formData.append('status', $('#status').is(':checked'));
        
        $.ajax({
            type: 'POST',
            url: cadastrar_funcionario_url,
            data: new URLSearchParams(formData).toString(),
            headers: {
                'X-CSRFToken': $('[name=csrfmiddlewaretoken]').val(),
                'Content-Type': 'application/x-www-form-urlencoded'
            },
            success: function(response) {
                if (response.success) {
                    var statusClass = response.funcionario.status ? 'ativo' : 'inativo';
                    var statusText = response.funcionario.status ? 'ATIVO' : 'INATIVO';
                    
                    // Adiciona o novo funcionário à tabela
                    $('#funcionario-list').append(`
                        <tr class="funcionario-row" data-id="${response.funcionario.id}">
                            <td>${response.funcionario.id}</td>
                            <td>${response.funcionario.nome}</td>
                            <td>${formatarCPF(response.funcionario.cpf)}</td>
                            <td>${response.funcionario.cargo}</td>
                            <td class="${statusClass}">${statusText}</td>
                            <td>
                                <button class="edit-btn" data-id="${response.funcionario.id}">Editar</button>
                            </td>
                        </tr>
                    `);
                    
                    // Fecha o modal e limpa o formulário
                    $('#modal').hide();
                    $('#funcionarioForm')[0].reset();
                    
                    // Mostra mensagem de sucesso
                    alert('Funcionário cadastrado com sucesso!');
                }
            },
            error: function(xhr) {
                console.error('Erro:', xhr);
                if (xhr.responseJSON && xhr.responseJSON.errors) {
                    $('.error-message').remove();
                    $('input, select').removeClass('input-error');
                    
                    if (typeof xhr.responseJSON.errors === 'string') {
                        alert(xhr.responseJSON.errors);
                    } else {
                        Object.keys(xhr.responseJSON.errors).forEach(function(key) {
                            const input = $(`[name="${key}"]`);
                            input.addClass('input-error');
                            input.after(`<div class="error-message">${xhr.responseJSON.errors[key]}</div>`);
                        });
                    }
                }
            }
        });
    });
});