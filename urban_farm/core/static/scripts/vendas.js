$(document).ready(function() {
    // Elementos do DOM
    var vendaForm = $('#vendaForm');
    var tipoSelect = $('#tipo');
    var documentoInput = $('#documento');
    var nomeInput = $('#nome');
    var razaoSocialInput = $('#razao_social');
    var nomeFantasiaInput = $('#nome_fantasia');
    var itensTable = $('#itensTable');
    var addItemBtn = $('#addItemBtn');
    var openModalBtn = $('#openModal');
    var closeModalBtn = $('.close');
    var viewModal = $('#viewModal');
    var vendaDetailsDiv = $('#vendaDetails');

    // Aplicar máscaras aos campos
    documentoInput.on('input', function() {
        var tipo = tipoSelect.val();
        if (tipo === 'PF') {
            $(this).mask('000.000.000-00', {
                reverse: true,
                clearIfNotMatch: true
            });
        } else if (tipo === 'PJ') {
            $(this).mask('00.000.000/0000-00', {
                reverse: true,
                clearIfNotMatch: true
            });
        }
    });

    // Evento quando o tipo de cliente muda
    tipoSelect.on('change', function() {
        var tipo = $(this).val();
        documentoInput.val(''); // Limpa o campo
        
        if (tipo === 'PF') {
            documentoInput.mask('000.000.000-00', {
                reverse: true,
                clearIfNotMatch: true
            });
            $('.pessoa-fisica').show();
            $('.pessoa-juridica').hide();
        } else if (tipo === 'PJ') {
            documentoInput.mask('00.000.000/0000-00', {
                reverse: true,
                clearIfNotMatch: true
            });
            $('.pessoa-juridica').show();
            $('.pessoa-fisica').hide();
        }
    });

    // Buscar cliente ao perder o foco do campo documento
    documentoInput.on('blur', function() {
        var tipo = tipoSelect.val();
        var documento = $(this).val();
        if (documento) {
            buscarCliente(tipo, documento);
        }
    });

    // Evento para adicionar novo item
    addItemBtn.on('click', function() {
        addItem();
    });

    // Eventos do modal
    openModalBtn.on('click', function() {
        resetForm();
        $('#modal').show();
    });

    closeModalBtn.on('click', function() {
        $('#modal').hide();
        resetForm();
    });

    $(window).on('click', function(event) {
        if ($(event.target).hasClass('modal')) {
            $(event.target).hide();
            resetForm();
        }
    });

    // Evento para ver detalhes da venda
    $(document).on('click', '.view-btn', function() {
        var vendaId = $(this).data('id');
        buscarVenda(vendaId);
    });

    // Evento de submissão do formulário
    vendaForm.on('submit', function(event) {
        event.preventDefault();
        if (validarFormulario()) {
            cadastrarVenda();
        }
    });

    // Eventos para cálculos dos itens
    $(document).on('change', '.produto-select', function() {
        var row = $(this).closest('tr');
        var preco = $(this).find(':selected').data('preco');
        row.find('.valor-unitario').val(preco);
        calcularSubtotal(row);
    });

    $(document).on('input', '.quantidade-input', function() {
        var row = $(this).closest('tr');
        calcularSubtotal(row);
    });

    $(document).on('click', '.remove-item', function() {
        $(this).closest('tr').remove();
        calcularTotal();
    });

    // Funções auxiliares
    function buscarCliente(tipo, documento) {
        // Mantém a formatação do documento ao invés de removê-la
        console.log("Buscando cliente:", tipo, documento);
        
        $.ajax({
            type: 'GET',
            url: buscar_cliente_url,
            data: {
                tipo: tipo,
                documento: documento  // Envia o documento formatado
            },
            success: function(data) {
                console.log("Resposta da busca de cliente:", data);
                if (data.cliente) {
                    if (tipo === 'PF') {
                        nomeInput.val(data.cliente.nome);
                    } else {
                        razaoSocialInput.val(data.cliente.razao_social);
                        nomeFantasiaInput.val(data.cliente.nome_fantasia);
                    }
                } else {
                    alert('Cliente não encontrado. Por favor, verifique os dados.');
                    resetClienteFields();
                }
            },
            error: function(xhr, status, error) {
                console.error("Erro na busca de cliente:", status, error);
                alert('Erro ao buscar cliente. Por favor, tente novamente.');
                resetClienteFields();
            }
        });
    }

    function cadastrarVenda() {
        $.ajax({
            type: 'POST',
            url: cadastrar_venda_url,
            data: vendaForm.serialize(),
            success: function(data) {
                console.log("Resposta da criação de venda:", data);
                if (data.venda) {
                    alert('Venda criada com sucesso!');
                    window.location.href = buscar_venda_url.replace('/0/', '/' + data.venda.id);
                } else {
                    alert('Erro ao criar venda. Por favor, verifique os dados.');
                }
            },
            error: function(xhr, status, error) {
                console.error("Erro ao criar venda:", status, error);
                alert('Erro ao criar venda. Por favor, tente novamente.');
            }
        });
    }

    function buscarVenda(vendaId) {
        $.ajax({
            type: 'GET',
            url: buscar_venda_url.replace('/0/', '/' + vendaId),
            success: function(data) {
                console.log("Resposta da busca de venda:", data);
                if (data.venda) {
                    vendaDetailsDiv.html('');
                    $.each(data.venda.itens, function(index, item) {
                        vendaDetailsDiv.append(`
                            <p>Produto: ${item.produto.nome}</p>
                            <p>Quantidade: ${item.quantidade}</p>
                            <p>Valor unitário: R$ ${item.valor_unitario}</p>
                            <p>Subtotal: R$ ${item.subtotal}</p>
                        `);
                    });
                    viewModal.modal('show');
                } else {
                    alert('Venda não encontrada. Por favor, verifique os dados.');
                }
            },
            error: function(xhr, status, error) {
                console.error("Erro na busca de venda:", status, error);
                alert('Erro ao buscar venda. Por favor, tente novamente.');
            }
        });
    }

    function addItem() {
        var newRow = $(`
            <tr>
                <td>
                    <select class="produto-select">
                        <option value="">Selecione um produto</option>
                    </select>
                </td>
                <td><input type="number" class="quantidade-input" value="1"></td>
                <td><input type="text" class="valor-unitario" readonly></td>
                <td><input type="text" class="subtotal" readonly></td>
                <td><button type="button" class="remove-item">Remover</button></td>
            </tr>
        `);
        
        var selectProduto = newRow.find('.produto-select');
        
        $.ajax({
            type: 'GET',
            url: listar_produtos_url,
            success: function(data) {
                console.log("Resposta da lista de produtos:", data);
                $.each(data, function(index, produto) {
                    selectProduto.append($('<option>', {
                        value: produto.id,
                        text: produto.nome,
                        'data-preco': produto.preco
                    }));
                });
            },
            error: function(xhr, status, error) {
                console.error("Erro na lista de produtos:", status, error);
                alert('Erro ao carregar produtos. Por favor, tente novamente.');
            }
        });
    
        itensTable.find('tbody').append(newRow);
    }

    function calcularSubtotal(row) {
        var quantidade = row.find('.quantidade-input').val();
        var valorUnitario = row.find('.valor-unitario').val();
        var subtotal = quantidade * valorUnitario;
        row.find('.subtotal').val(subtotal.toFixed(2));
        calcularTotal();
    }

    function calcularTotal() {
        var total = 0;
        itensTable.find('tr').each(function() {
            total += parseFloat($(this).find('.subtotal').val());
        });
        $('#total').val(total.toFixed(2));
    }

    function resetForm() {
        vendaForm.trigger('reset');
        resetClienteFields();
        itensTable.find('tr').not(':first').remove();
    }

    function resetClienteFields() {
        nomeInput.val('');
        razaoSocialInput.val('');
        nomeFantasiaInput.val('');
    }

    function listarProdutos() {
        $.ajax({
            type: 'GET',
            url: listar_produtos_url,
            success: function(data) {
                console.log("Resposta da lista de produtos:", data);
                var options = '';
                $.each(data.produtos, function(index, produto) {
                    options += `<option value="${produto.id}" data-preco="${produto.preco}">${produto.nome}</option>`;
                });
                return options;
            },
            error: function(xhr, status, error) {
                console.error("Erro na lista de produtos:", status, error);
                alert('Erro ao carregar produtos. Por favor, tente novamente.');
            }
        });
    }

    function validarFormulario() {
        // Implementar lógica de validação do formulário
        return true;
    }
});