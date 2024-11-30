class PlantFilter {
    constructor(searchInputId, stageFilterId, tableBodyId) {
        this.searchInput = document.getElementById(searchInputId);
        this.stageFilter = document.getElementById(stageFilterId);
        this.tableBody = document.getElementById(tableBodyId);

        this.init();
    }

    init() {
        this.searchInput.addEventListener('keyup', () => this.filterPlants());
        this.stageFilter.addEventListener('change', () => this.filterPlants());
    }

    filterPlants() {
        const filter = this.searchInput.value.toLowerCase();
        const stageFilter = this.stageFilter.value;
        const rows = this.tableBody.getElementsByTagName('tr');

        for (let i = 0; i < rows.length; i++) {
            const cells = rows[i].getElementsByTagName('td');
            let found = false;

            // Filtragem pelo nome da planta
            for (let j = 0; j < cells.length; j++) {
                const cell = cells[j];
                if (cell && cell.textContent.toLowerCase().includes(filter)) {
                    found = true;
                    break;
                }
            }

            // Filtragem pelo estágio
            const estagio = rows[i].getAttribute('data-estagio');
            if (stageFilter && estagio !== stageFilter) {
                found = false;
            }

            rows[i].style.display = found ? '' : 'none';
        }
    }
}

// Instância da classe PlantFilter
document.addEventListener('DOMContentLoaded', () => {
    new PlantFilter('search', 'stage-filter', 'plant-table-body');
});