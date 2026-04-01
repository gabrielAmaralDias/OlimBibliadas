async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    try {
        const res = await fetch("/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password })
        });

        const data = await res.json();

        if (res.status === 200) {
            localStorage.setItem("token", data.access_token);
            window.location.href = "/index.html";
        } else {
            document.getElementById("msg").innerText = data.erro || "Login inválido";
        }
    } catch (error) {
        document.getElementById("msg").innerText = "Erro ao conectar com servidor";
    }
}

function sair() {
    localStorage.removeItem("token");
    window.location.href = "/login.html";
}

// Protege o index — redireciona para login se não tiver token
function verificarLogin() {
    const paginaAtual = window.location.pathname;
    const token = localStorage.getItem("token");

    if (paginaAtual.includes("index") && !token) {
        window.location.href = "/login.html";
    }
}

let perguntaAtual = null;
let mostrandoResposta = false;

function extrairTexto(registro, chavesPreferidas) {
    if (!registro || typeof registro !== "object") return "";
    for (const chave of chavesPreferidas) {
        const valor = registro[chave];
        if (typeof valor === "string" && valor.trim()) return valor;
    }
    const chaves = Object.keys(registro);
    for (const chave of chaves) {
        const valor = registro[chave];
        if (typeof valor === "string" && valor.trim()) return valor;
    }
    return "";
}

function renderCard() {
    const front = document.querySelector(".card-front");
    const back = document.querySelector(".card-back");
    if (!front || !back) return;

    if (!perguntaAtual) {
        front.innerText = "Sem perguntas";
        back.innerText = "";
        return;
    }

    const textoPergunta = extrairTexto(perguntaAtual, ["Pergunta", "question", "titulo", "enunciado"]);
    const textoResposta = extrairTexto(perguntaAtual, ["Reposta", "answer", "solucao", "resolucao"]);

    front.innerText = textoPergunta || JSON.stringify(perguntaAtual, null, 2);
    back.innerText = textoResposta || "Sem resposta cadastrada";
}

async function carregarPergunta() {
    const card = document.getElementById("card");
    if (!card) return;

    mostrandoResposta = false;
    card.classList.remove("flip");

    const front = document.querySelector(".card-front");
    if (front) front.innerText = "Carregando...";

    try {
        const res = await fetch("/pergunta");
        const data = await res.json();

        if (!res.ok) {
            perguntaAtual = null;
            if (front) front.innerText = data?.erro || "Erro ao carregar pergunta";
            return;
        }

        perguntaAtual = data;
        renderCard();
    } catch (error) {
        if (front) front.innerText = "Erro ao conectar com servidor";
    }
}

function virar() {
    if (!perguntaAtual) return;
    const card = document.getElementById("card");
    card.classList.toggle("flip");
}

function proxima() {
    carregarPergunta();
}

document.addEventListener("DOMContentLoaded", () => {
    verificarLogin();
    if (document.getElementById("card")) {
        carregarPergunta();
    }
});