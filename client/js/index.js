const API_URL = `${window.location.protocol}//${window.location.hostname.replace(
    "-5500",
    "-5000"
)}`;

const listaMaterias = document.getElementById("listaMaterias");
const campoPesquisa = document.getElementById("campoPesquisa");

let materias = [];

async function carregarMaterias() {
    try {
        const response = await fetch(`${API_URL}/materias`);
        const data = await response.json();

        materias = data.materias;

        renderizarMaterias(materias);

    } catch (error) {
        console.error("Erro ao carregar matérias:", error);

        listaMaterias.innerHTML = `
            <div class="col-12">
                <div class="alert alert-danger">
                    Não foi possível carregar as matérias.
                </div>
            </div>
        `;
    }
}

function renderizarMaterias(lista) {

    listaMaterias.innerHTML = "";

    if (lista.length === 0) {

        listaMaterias.innerHTML = `
            <div class="col-12">
                <div class="subject-card">
                    Nenhuma matéria encontrada.
                </div>
            </div>
        `;

        return;
    }

    lista.forEach(materia => {

        listaMaterias.innerHTML += `
            <div class="col-12 col-md-6">
                <div class="subject-card">
                    <div class="subject-title">
                        ${materia.nome}
                    </div>

                    <div class="subject-term">
                        ${materia.codigo}
                    </div>

                    <div class="subject-meta">
                        ${materia.departamento}
                    </div>
                </div>
            </div>
        `;
    });
}

campoPesquisa.addEventListener("input", () => {

    const texto = campoPesquisa.value.toLowerCase();

    const filtradas = materias.filter(materia =>
        materia.nome.toLowerCase().includes(texto) ||
        materia.codigo.toLowerCase().includes(texto) ||
        materia.departamento.toLowerCase().includes(texto)
    );

    renderizarMaterias(filtradas);
});

carregarMaterias();