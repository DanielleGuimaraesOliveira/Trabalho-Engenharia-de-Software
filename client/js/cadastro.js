const nomeInput = document.getElementById("nome");
const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const confirmarSenhaInput = document.getElementById("confirmarSenha");
const btnCadastrar = document.getElementById("btnCadastrar");

const API_URL = `${window.location.protocol}//${window.location.hostname.replace(
    "-5500",
    "-5000"
)}`;

btnCadastrar.addEventListener("click", async () => {

    const nome = nomeInput.value.trim();
    const email = emailInput.value.trim();
    const senha = senhaInput.value;
    const confirmarSenha = confirmarSenhaInput.value;

    if (!nome || !email || !senha || !confirmarSenha) {
        alert("Preencha todos os campos.");
        return;
    }

    if (senha !== confirmarSenha) {
        alert("As senhas não coincidem.");
        return;
    }

    try {

        const response = await fetch(`${API_URL}/aluno`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                nome: nome,
                email: email,
                senha: senha
            })
        });

        const data = await response.json();

        if (response.ok) {

            alert("Cadastro realizado com sucesso!");

            window.location.href = "login.html";

        } else {

            alert(data.message || "Erro ao cadastrar.");
        }

    } catch (error) {

        console.error(error);

        alert("Erro ao conectar com o servidor.");
    }
});