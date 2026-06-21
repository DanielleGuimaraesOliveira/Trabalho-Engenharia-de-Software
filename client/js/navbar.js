async function carregarNavbar() {
    const navbarPath =
        window.location.pathname.includes("/html/")
            ? "../navbar.html"
            : "navbar.html";

    const response = await fetch(navbarPath);
    const html = await response.text();

    document.getElementById("navbar").innerHTML = html;

    console.log("Navbar carregada");

    const token = localStorage.getItem("token");
    console.log("Token:", token);

    const homeLink = document.getElementById("homeLink");

    if (homeLink) {
        homeLink.href = window.location.pathname.includes("/html/")
            ? "../index.html"
            : "index.html";
    }
        const btnLogin = document.getElementById("btnLogin");

    if (btnLogin) {
        btnLogin.href = window.location.pathname.includes("/html/")
            ? "login.html"
            : "html/login.html";
    }
    console.log("Botão:", btnLogin);

    if (token && btnLogin) {
        btnLogin.remove();
    }
}

carregarNavbar();