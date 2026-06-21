const API_URL = "http://localhost:5000";

const nomeAlunoLabel = document.getElementById("nomeAlunoLabel");
const nomeMateriaEl = document.getElementById("nomeMateria");
const campoComentario = document.getElementById("campoComentario");
const notaValorEl = document.getElementById("notaValor");
const btnNotaUp = document.getElementById("btnNotaUp");
const btnNotaDown = document.getElementById("btnNotaDown");
const btnPostar = document.getElementById("btnPostar");
const mensagemErro = document.getElementById("mensagemErro");

const NOTA_MINIMA = 1;
const NOTA_MAXIMA = 5;

let nota = 3;

const params = new URLSearchParams(window.location.search);
const materiaId = params.get("materia_id");

const token = localStorage.getItem("token");

function decodificaPayloadToken(jwtToken) {
    try {
        const partes = jwtToken.split(".");
        const payloadBase64 = partes[1].replace(/-/g, "+").replace(/_/g, "/");
        const payloadJson = decodeURIComponent(
            atob(payloadBase64)
                .split("")
                .map(c => "%" + c.charCodeAt(0).toString(16).padStart(2, "0"))
                .join("")
        );

        return JSON.parse(payloadJson);

    } catch (error) {
        return null;
    }
}

function mostraErro(texto) {
    mensagemErro.textContent = texto;
    mensagemErro.classList.remove("d-none");
}

function escondeErro() {
    mensagemErro.classList.add("d-none");
}

function atualizaNotaDisplay() {
    notaValorEl.textContent = nota;
}

btnNotaUp.addEventListener("click", () => {
    if (nota < NOTA_MAXIMA) {
        nota += 1;
        atualizaNotaDisplay();
    }
});

btnNotaDown.addEventListener("click", () => {
    if (nota > NOTA_MINIMA) {
        nota -= 1;
        atualizaNotaDisplay();
    }
});

async function carregarNomeAluno() {
    try {
        console.log("Token:", token);

        const response = await fetch(`${API_URL}/aluno/me`, {
            headers: {
                Authorization: `Bearer ${token}`
            }
        });

        const data = await response.json();

        console.log("Status:", response.status);
        console.log("Resposta:", JSON.stringify(data));

        if (!response.ok) {
            throw new Error(data.message);
        }

        nomeAlunoLabel.textContent = data.nome;

    } catch (error) {
        console.error("Erro ao carregar aluno:", error);
        nomeAlunoLabel.textContent = "Aluno";
    }
}
async function carregarNomeMateria() {
    try {
        const response = await fetch(`${API_URL}/materias/${materiaId}`);

        if (!response.ok) {
            throw new Error("Matéria não encontrada");
        }

        const materia = await response.json();

        nomeMateriaEl.textContent = materia.nome;

    } catch (error) {
        console.error("Erro ao carregar matéria:", error);
        nomeMateriaEl.textContent = "Matéria não encontrada";
    }
}

btnPostar.addEventListener("click", async () => {

    escondeErro();

    const comentario = campoComentario.value.trim();

    if (!comentario) {
        mostraErro("Escreva um comentário antes de postar.");
        return;
    }

    const payload = decodificaPayloadToken(token);

    if (!payload || !payload.sub) {
        mostraErro("Sessão inválida. Faça login novamente.");
        return;
    }

    btnPostar.disabled = true;

    try {
        const response = await fetch(`${API_URL}/review`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`
            },
            body: JSON.stringify({
                comentario,
                nota,
                id_aluno: payload.sub,
                id_materia: Number(materiaId)
            })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.message || "Não foi possível publicar a review.");
        }

        window.location.href = `materia.html?id=${materiaId}`;

    } catch (error) {
        console.error("Erro ao postar review:", error);
        mostraErro(error.message);

    } finally {
        btnPostar.disabled = false;
    }
});

if (!token) {

    window.location.href = "login.html";

} else if (!materiaId) {

    mostraErro("Matéria não informada.");
    btnPostar.disabled = true;

} else {

    atualizaNotaDisplay();
    carregarNomeAluno();
    carregarNomeMateria();
}
