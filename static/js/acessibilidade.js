document.addEventListener("DOMContentLoaded", function () {
    const botao = document.getElementById("botao-acessibilidade");

    if (!botao) return;

    const fonteAmpliada = localStorage.getItem("fonteAmpliada") === "true";

    function atualizarAcessibilidade(ativo) {
        document.body.classList.toggle("fonte-ampliada", ativo);

        botao.textContent = ativo ? "A- Fonte normal" : "A+ Aumentar fonte";
        botao.setAttribute("aria-pressed", ativo);
    }

    atualizarAcessibilidade(fonteAmpliada);

    botao.addEventListener("click", function () {
        const ativo = !document.body.classList.contains("fonte-ampliada");

        localStorage.setItem("fonteAmpliada", ativo);
        atualizarAcessibilidade(ativo);
    });
});