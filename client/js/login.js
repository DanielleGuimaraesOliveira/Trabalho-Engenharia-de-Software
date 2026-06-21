const emailInput = document.getElementById("email");
const senhaInput = document.getElementById("senha");
const btnLogin = document.getElementById("btnEntrar");

// const API_URL = `${window.location.protocol}//${window.location.hostname.replace(
//     "-5500",
//     "-5000"
// )}`;

const API_URL = "http://localhost:5000";

btnLogin.addEventListener("click", async () => {

    const email = emailInput.value;
    const senha = senhaInput.value;

    try {
        const response = await fetch(`${API_URL}/login`, { method: "POST", headers: { "Content-Type": "application/json"},
        body: JSON.stringify({email, senha})
        });

    const data = await response.json();

    if (response.ok) {
        localStorage.setItem("token", data.token);
        console.log("Token salvo:", data.token);

        window.location.href = "../index.html";

    } else {

        alert(data.message);
    }

    } catch (error) {

        console.error(error);

        alert("Erro ao conectar com o servidor.");
    }
});