let userName = "";
let currentAudio = null; // Track the currently playing audio

function submitName() {
    const nameInput = document.getElementById("userName");
    userName = nameInput.value.trim();

    if (userName) {
        const greeting = document.getElementById("greeting");
        greeting.textContent = `Hi, ${userName}!`;

        const nameEntry = document.getElementById("nameEntry");
        nameEntry.classList.add("hidden");

        const chatInterface = document.getElementById("chatInterface");
        chatInterface.classList.remove("hidden");

        fetch("/greet", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name: userName })
        })
            .then(response => response.json())
            .then(data => {
                const chatBox = document.getElementById("chatBox");
                const botMessageDiv = document.createElement("div");
                
                // Clean SSML before displaying
                botMessageDiv.textContent = cleanSSML(data.reply);
                botMessageDiv.classList.add("bot-message");
                chatBox.appendChild(botMessageDiv);
        
                if (data.audio_url) {
                    playAudio(data.audio_url);
                }
            })
            .catch(error => console.error("Error:", error));
        
    }
}

function sendMessage() {
    const userInput = document.getElementById("userInput").value.trim();

    if (!userInput) return;

    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userInput, name: userName })
    })
        .then(response => response.json())
        .then(data => {
            const chatBox = document.getElementById("chatBox");

            const botMessage = document.createElement("div");
            botMessage.textContent = data.reply || "I'm sorry, I couldn't generate a response.";
            botMessage.classList.add("bot-message");
            chatBox.appendChild(botMessage);

            if (data.audio_url) {
                playAudio(data.audio_url);
            }
        })
        .catch(error => console.error("Error:", error));
}


function playAudio(audioUrl) {
    // Stop any currently playing audio
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0;
    }

    // Play new audio
    currentAudio = new Audio(audioUrl);

    // Show the stop button while audio is playing
    const stopButton = document.getElementById("stopButton");
    stopButton.style.display = "inline-block";

    currentAudio.play();

    currentAudio.onended = function () {
        stopButton.style.display = "none"; // Hide the stop button when audio ends
        currentAudio = null;
    };

    currentAudio.onpause = function () {
        stopButton.style.display = "none"; // Hide the stop button when audio is paused
    };
}

function stopAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio.currentTime = 0; // Reset playback to the beginning
        currentAudio = null;

        // Hide the stop button
        const stopButton = document.getElementById("stopButton");
        stopButton.style.display = "none";
    }
}

// Voice recognition logic remains unchanged
const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
recognition.lang = "en-US";

function startVoice() {
    recognition.start();
}

recognition.onresult = function (event) {
    const userMessage = event.results[0][0].transcript.trim();

    // Display the user's voice message
    const chatBox = document.getElementById("chatBox");
    const userMessageDiv = document.createElement("div");
    userMessageDiv.textContent = userMessage;
    userMessageDiv.classList.add("user-message");
    chatBox.appendChild(userMessageDiv);

    // Send the message to the server
    fetch("/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: userMessage, name: userName })
    })
        .then(response => response.json())
        .then(data => {
            const botMessage = document.createElement("div");
            botMessage.textContent = data.reply;
            botMessage.classList.add("bot-message");
            chatBox.appendChild(botMessage);

            if (data.audio_url) {
                playAudio(data.audio_url);
            }
        })
        .catch(error => console.error("Error:", error));
};


// Function to clean SSML tags from the response
function cleanSSML(ssml) {
    return ssml.replace(/<[^>]+>/g, ""); // Removes all tags within < and >
}
