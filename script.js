const input = document.getElementById("userInput");
const chatBox = document.getElementById("chatBox");

/* -------------------------
   BASIC MESSAGE ADD
------------------------- */
function addMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "message " + sender;
    div.innerText = text;
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
}

/* -------------------------
   THINKING INDICATOR
------------------------- */
function addThinking() {
    const div = document.createElement("div");
    div.className = "message ai thinking";
    div.innerText = "MPAI is thinking...";
    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    return div;
}

function removeThinking(div) {
    if (div) div.remove();
}

/* -------------------------
   TYPING EFFECT
------------------------- */
function typeMessage(text, sender) {
    const div = document.createElement("div");
    div.className = "message " + sender;
    chatBox.appendChild(div);

    let i = 0;
    const interval = setInterval(() => {
        div.innerText += text.charAt(i);
        i++;
        chatBox.scrollTop = chatBox.scrollHeight;
        if (i >= text.length) clearInterval(interval);
    }, 20);
}

/* -------------------------
   SEND MESSAGE
------------------------- */
async function sendMessage() {
    const message = input.value.trim();
    if (!message) return;

    input.value = "";
    addMessage(message, "user");

    const thinkingDiv = addThinking();

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message })
        });

        const data = await res.json();
        removeThinking(thinkingDiv);
        typeMessage(data.reply, "ai");

    } catch (err) {
        removeThinking(thinkingDiv);
        addMessage("⚠️ Server error", "ai");
    }
}

/* -------------------------
   ENTER KEY
------------------------- */
input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
});
