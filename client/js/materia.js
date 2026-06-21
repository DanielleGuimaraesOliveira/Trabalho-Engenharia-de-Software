const API_URL = "http://localhost:5000";

const materiaHeader = document.getElementById("materiaHeader");
const listaReviews = document.getElementById("listaReviews");

const params = new URLSearchParams(window.location.search);
const materiaId = params.get("id");

async function carregarMateria() {
    try {
        const response = await fetch(`${API_URL}/materias/${materiaId}`);

        if (!response.ok) {
            throw new Error("Matéria não encontrada");
        }

        const materia = await response.json();

        renderizarHeader(materia);

    } catch (error) {
        console.error("Erro ao carregar matéria:", error);

        materiaHeader.innerHTML = `
            <div class="alert alert-danger mb-0">
                Não foi possível carregar a matéria.
            </div>
        `;
    }
}

async function carregarReviews() {
    try {
        const response = await fetch(`${API_URL}/reviews?materia_id=${materiaId}`);
        const data = await response.json();

        renderizarReviews(data.reviews);

    } catch (error) {
        console.error("Erro ao carregar reviews:", error);

        listaReviews.innerHTML = `
            <div class="alert alert-danger mb-0">
                Não foi possível carregar as reviews.
            </div>
        `;
    }
}

function renderizarHeader(materia) {

    materiaHeader.innerHTML = `
        <div>
            <div class="materia-title">${materia.nome}</div>
            <div class="materia-meta">Departamento: <strong>${materia.departamento}</strong></div>
        </div>

        <button type="button" class="btn-add-review" id="btnAdicionarReview">
            <i class="bi bi-plus-lg"></i> Adicionar Review
        </button>
    `;

    document
        .getElementById("btnAdicionarReview")
        .addEventListener("click", () => {
            window.location.href = `nova-review.html?materia_id=${materiaId}`;
        });
}

function renderizarReviews(reviews) {

    listaReviews.innerHTML = "";

    if (!reviews || reviews.length === 0) {

        listaReviews.innerHTML = `
            <div class="review-empty">
                Ainda não há reviews para essa matéria.
            </div>
        `;

        return;
    }

    reviews.forEach(review => {

        const autor = review.nome_aluno || "Aluno";

        listaReviews.innerHTML += `
            <div class="review-card">
                <div>
                    <div class="review-author">${autor}</div>
                    <div class="review-comment">${review.comentario}</div>
                </div>

                <div class="review-score">${review.nota}/10</div>
            </div>
        `;
    });
}

if (!materiaId) {

    materiaHeader.innerHTML = `
        <div class="alert alert-danger mb-0">
            Matéria não informada.
        </div>
    `;

} else {

    carregarMateria();
    carregarReviews();
}
