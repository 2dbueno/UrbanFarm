// Inicializa o modo escuro com base na preferência do usuário ou no tema do sistema
function initDarkMode() {
    const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)");
    const storedTheme = localStorage.getItem('theme');

    // Define o tema inicial com base no armazenamento ou na preferência do sistema
    if (storedTheme === 'dark' || (storedTheme === null && prefersDarkScheme.matches)) {
        document.body.classList.add('dark');
    }
}

// Alterna o modo escuro e atualiza o armazenamento local
function toggleDarkMode() {
    document.body.classList.toggle('dark');

    // Atualiza o tema armazenado
    if (document.body.classList.contains('dark')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
}

// Configura ouvintes de eventos
function setupEventListeners() {
    const themeToggleButton = document.getElementById('theme-toggle');
    if (themeToggleButton) {
        themeToggleButton.addEventListener('click', toggleDarkMode);
    }
}

// Função de inicialização
function init() {
    initDarkMode();
    setupEventListeners();
}

// Aguarda o carregamento do DOM
document.addEventListener('DOMContentLoaded', init);
