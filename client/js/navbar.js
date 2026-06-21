async function carregarNavbar() {

    const navbarPath =
        window.location.pathname.includes("/html/")
            ? "../navbar.html"
            : "navbar.html";

    const response = await fetch(navbarPath);

    const html = await response.text();

    document.getElementById("navbar").innerHTML = html;

    const token = localStorage.getItem("token");

    if (token) {
        const btnLogin = document.getElementById("btnLogin");

        if (btnLogin) {
            btnLogin.remove();
        }
    }
}

carregarNavbar();