const API_URL = "http://127.0.0.1:8000/ask";

// elementos do DOM
const chatContainer = document.getElementById("chat-container");
const inputField = document.getElementById("user-input");
const sendButton = document.getElementById("send-btn");

// ==============================
//  SIDEBAR
// ==============================
function updateSidebar(profile, insights) {
    if (!profile) return;

    const setText = (id, value) => {
        const el = document.getElementById(id);
        if (el) el.innerText = value ?? "-";
    };

    setText("user-name", profile.nome);
    setText("user-age", profile.idade);
    setText("user-profession", profile.profissao);
    setText("user-income", profile.renda_mensal);
    setText("user-profile", profile.perfil_investidor);
    setText("user-wealth", profile.patrimonio_total);

    const insightsBox = document.getElementById("user-insights");

    if (insightsBox && insights) {
        insightsBox.innerHTML = renderInsights(insights);
    }
}

// ==============================
//  INSIGHTS
// ==============================
function renderInsights(insights) {
    if (!insights) return "-";

    const progress = insights.goals_progress?.total_meta
        ? (insights.goals_progress.patrimonio / insights.goals_progress.total_meta) * 100
        : 0;

    const healthClass =
        insights.emergency_health === "boa" ? "status-ok" :
        insights.emergency_health === "media" ? "status-warning" :
        "status-bad";

    return `
        <div class="insight-card">

            <div class="insight-row">
                <span class="insight-label">📊 Reserva</span>
                <span class="insight-value ${healthClass}">
                    ${insights.emergency_health || "-"}
                </span>
            </div>

            <div class="insight-row">
                <span class="insight-label">⚖️ Estratégia</span>
                <span class="insight-value">
                    ${insights.risk_advice || "-"}
                </span>
            </div>

            <div class="insight-meta">
                🎯 ${insights.goals_progress?.patrimonio || 0} / ${insights.goals_progress?.total_meta || 0}
            </div>

            <div class="progress-bar">
                <div class="progress-fill" style="width: ${progress}%"></div>
            </div>

        </div>
    `;
}

// ==============================
//  FORMATADOR
// ==============================
function formatMessage(text) {
    if (!text) return "";

    return text
        .replace(/\n\s+/g, "\n")
        .replace(/\n/g, "<br>")
        .replace(/💡 (.*?)<br>/g, "<strong>💡 $1</strong><br><br>")
        .replace(/Resumo:/g, "<strong>Resumo:</strong>")
        .replace(/Exemplo:/g, "<strong>Exemplo:</strong>")
        .replace(/Em termos simples:/g, "<strong>Em termos simples:</strong>");
}

// ==============================
//  MENSAGEM
// ==============================
function createMessage(text, sender = "bot") {
    const message = document.createElement("div");
    message.classList.add("message", sender);

    if (typeof text === "object") {
        message.textContent = JSON.stringify(text, null, 2);
    } else {
        message.innerHTML = formatMessage(text);
    }

    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ==============================
//  LOADING
// ==============================
function createLoadingMessage() {
    const message = document.createElement("div");
    message.classList.add("message", "bot", "loading");
    message.innerText = "Thinking...";
    chatContainer.appendChild(message);
    chatContainer.scrollTop = chatContainer.scrollHeight;
    return message;
}

// ==============================
//  PARSE RESPONSE
// ==============================
function extractResponse(data) {
    if (!data) return "No response from server.";

    if (typeof data === "string") return data;

    if (data.response && data.response.content) {
        return data.response.content;
    }

    if (typeof data.answer === "string") return data.answer;
    if (typeof data.response === "string") return data.response;
    if (typeof data.message === "string") return data.message;

    return JSON.stringify(data, null, 2);
}

// ==============================
//  DETECTOR DE QUIZ
// ==============================
function detectQuiz(data) {
    if (!data) return null;

    // formato esperado
    if (data.response && data.response.type === "quiz") {
        return data.response;
    }

    // fallback: quiz veio direto
    if (data.type === "quiz") {
        return data;
    }

    // fallback: quiz dentro de response como objeto cru
    if (data.response && typeof data.response === "object") {
        if (data.response.question && data.response.options) {
            return data.response;
        }
    }

    return null;
}

// =============================
//  ENVIO
// ==============================
async function sendMessage() {
    const userText = inputField.value.trim();
    if (!userText) return;

    createMessage(userText, "user");
    inputField.value = "";

    const loadingMessage = createLoadingMessage();

    try {
        const response = await fetch(API_URL, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: userText
            })
        });

        const data = await response.json();
        loadingMessage.remove();

        // ==============================
        //  QUIZ DETECTION 
        // ==============================
        const quizData = detectQuiz(data);

        if (quizData) {
            renderQuiz(quizData);
        } else {
            const botText = extractResponse(data);
            createMessage(botText, "bot");
        }

        // ==============================
        //  SIDEBAR
        // ==============================
        if (data.user_profile) {
            updateSidebar(data.user_profile, data.insights);
        }

    } catch (error) {
        loadingMessage.remove();
        createMessage("Erro ao conectar com o backend.", "bot");
        console.error(error);
    }
}

// ==============================
//  QUIZ (UPGRADED)
// ==============================
function renderQuiz(data) {
    if (!data || !data.question) return;

    const container = document.createElement("div");
    container.classList.add("message", "bot");

    const question = document.createElement("p");
    question.innerHTML = `<b>🧠 Quiz:</b><br>${data.question}`;
    container.appendChild(question);

    const optionsContainer = document.createElement("div");
    optionsContainer.style.display = "flex";
    optionsContainer.style.flexDirection = "column";
    optionsContainer.style.gap = "10px";
    optionsContainer.style.marginTop = "12px";

    let answered = false;

    (data.options || []).forEach(option => {
        const btn = document.createElement("button");
        btn.innerText = option;
        btn.classList.add("quiz-option");

        btn.onclick = () => {
            if (answered) return;
            answered = true;

            const isCorrect = option === data.correct;

            btn.classList.add(isCorrect ? "quiz-correct" : "quiz-wrong");

            if (isCorrect) {
                createMessage("✅ Excelente! Você acertou.", "bot");
            } else {
                createMessage(`❌ Não foi dessa vez.<br><b>Resposta correta:</b> ${data.correct}`, "bot");
            }

            optionsContainer.querySelectorAll("button").forEach(b => {
                b.disabled = true;

                if (b.innerText === data.correct) {
                    b.classList.add("quiz-correct");
                }
            });
        };

        optionsContainer.appendChild(btn);
    });

    container.appendChild(optionsContainer);
    chatContainer.appendChild(container);
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// ==============================
//  EVENTOS
// ==============================
sendButton.addEventListener("click", sendMessage);

inputField.addEventListener("keypress", function (e) {
    if (e.key === "Enter") {
        sendMessage();
    }
});