document.addEventListener('DOMContentLoaded', function() {
    const openModalButton = document.getElementById('openModal');
    const modal = document.getElementById('modal');
    const closeModalButton = document.querySelector('.close');
    const addItemButton = document.getElementById('addItem');
    const vendaForm = document.getElementById('vendaForm');
    const itensList = document.getElementById('itens-list');
    const precoTotalInput = document.getElementById('preco_total');
    let itemCount = 0;
    let totalPrice = 0;

    openModalButton.addEventListener('click', function() {
        modal.style.display = 'block';
    });

    closeModalButton.addEventListener('click', function() {
        modal.style.display = 'none';
    });

    addItemButton.addEventListener('click', function() {
        const itemInput = document.getElementById('item');
        const quantidadeInput = document.getElementById('quantidade');
        const valorUnitarioInput = document.getElementById('valor_unitario');
    
        const item = itemInput.value;
        const quantidade = parseInt(quantidadeInput.value);
        const valorUnitario = parseFloat(valorUnitarioInput.value);
    
        // Verifica se os campos são válidos
        if (item && !isNaN(quantidade) && !isNaN(valorUnitario) && quantidade > 0 && valorUnitario > 0) {
            const row = itensList.insertRow();
            row.innerHTML = `<td>${item}</td><td>${quantidade}</td><td>R$ ${valorUnitario.toFixed(2)}</td>`;
            itemCount++;
            
            // Atualiza o preço total
            totalPrice += (quantidade * valorUnitario);
            precoTotalInput.value = totalPrice.toFixed(2);
    
            // Limpa os campos de entrada
            itemInput.value = '';
            quantidadeInput.value = '';
            valorUnitarioInput.value = '';
        } else {
            alert('Por favor, preencha todos os campos corretamente.');
        }
    });

    vendaForm.addEventListener('submit', function(event) {
        event.preventDefault();
        const formData = new FormData(vendaForm);
        formData.append('item_count', itemCount);

        // Adiciona os itens à FormData
        for (let i = 0; i < itemCount; i++) {
            const row = itensList.rows[i];
            const item = row.cells[0].innerText;
            const quantidade = row.cells[1].innerText;
            const valorUnitario = row.cells[2].innerText.replace('R$ ', '').replace(',', '.'); // Remove o símbolo e formata

            formData.append(`itens-${i}-item`, item);
            formData.append(`itens-${i}-quantidade`, quantidade);
            formData.append(`itens-${i}-valor_unitario`, valorUnitario);
        }

        fetch(cadastrar_venda_url, {
            method: 'POST',
            body: formData,
        })
        .then(response => {
            // Verifica se a resposta é OK (status 200-299)
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.errors); });
            }
            return response.json();
        })
        .then(data => {
            if (data.success) {
                alert('Venda cadastrada com sucesso! ID da Venda: ' + data.venda_id);
                location.reload(); // Recarrega a página para mostrar a nova venda
            } else {
                alert('Erro ao cadastrar venda: ' + JSON.stringify(data.errors));
            }
        })
        .catch(error => {
            console.error('Erro:', error);
            alert('Ocorreu um erro ao cadastrar a venda: ' + error.message);
        });
    });

    // Função para editar e excluir vendas
    document.querySelectorAll('.edit-btn').forEach(button => {
        button.addEventListener('click', function() {
            const vendaId = this.getAttribute('data-id');
            fetch(buscar_venda_url.replace('/0/', `/${vendaId}`))
                .then(response => {
                    if (!response.ok) {
                        return response.text().then(text => { throw new Error(text); });
                    }
                    return response.json();
                })
                .then(data => {
                    // Preenche o formulário com os dados da venda
                    document.getElementById('cliente').value = data.venda.cliente;
                    precoTotalInput.value = data.venda.preco_total;
                    // Adiciona os itens ao formulário
                    data.itens.forEach(item => {
                        const row = itensList.insertRow();
                        row.innerHTML = `<td>${item.item}</td><td>${item.quantidade}</td><td>R$ ${item.valor_unitario.toFixed(2)}</td>`;
                    });
                    modal.style.display = 'block';
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Ocorreu um erro ao buscar a venda: ' + error.message);
                });
        });
    });

    document.querySelectorAll('.delete-btn').forEach(button => {
        button.addEventListener('click', function() {
            const vendaId = this.getAttribute('data-id');
            if (confirm('Tem certeza que deseja deletar esta venda?')) {
                fetch(`/deletar-venda/${vendaId}/`, {
                    method: 'POST',
                    headers: {
                        'X-CSRFToken': getCookie('csrftoken'),
                    },
                })
                .then(response => response.json())
                .then(data => {
                    if (data.success) {
                        alert('Venda deletada com sucesso!');
                        location.reload(); // Recarrega a página para atualizar a lista
                    } else {
                        alert('Erro ao deletar venda.');
                    }
                })
                .catch(error => {
                    console.error('Erro:', error);
                    alert('Ocorreu um erro ao deletar a venda.');
                });
            }
        });
    });
});

// Função para obter o cookie CSRF
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Verifica se este cookie começa com o nome que estamos procurando
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}