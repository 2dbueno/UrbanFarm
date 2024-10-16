class NavManager {
    constructor() {
        // Inicializa o gerenciamento de navegação
        this.sidebarLinks = document.querySelectorAll('.sidebar ul li a'); // Seleciona todos os links na sidebar
        this.highlightActiveLink(); // Executa a função de destaque do link ativo
    }

    // Função para verificar e destacar o link ativo
    highlightActiveLink() {
        // Obtém a URL da página atual (sem o domínio)
        const currentPath = window.location.pathname;

        // Percorre cada link da barra lateral
        this.sidebarLinks.forEach(link => {
            // Verifica se o href do link corresponde ao caminho atual
            if (link.getAttribute('href') === currentPath) {
                link.classList.add('active-link'); // Adiciona a classe ativa ao link correspondente
            }
        });
    }
}

// Instancia a classe NavManager quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', () => {
    new NavManager(); // Executa a classe para gerenciar a navegação
});
