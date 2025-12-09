const micButton = document.getElementById('micButton');
const sendButton = document.getElementById('sendButton');
const textInput = document.getElementById('textInput');
const statusDiv = document.getElementById('status');
const visualizer = document.getElementById('visualizer');
const chatHistory = document.getElementById('chat-history');
const stopButton = document.getElementById('stopButton');
const langToggle = document.getElementById('langToggle');

let isListening = false;
let recognition = null;
let currentLang = 'en-US';

// Initialize Speech Recognition
if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = currentLang;

    recognition.onstart = () => {
        isListening = true;
        micButton.classList.add('listening');
        statusDiv.textContent = currentLang === 'hi-IN' ? "सुन रहा हूँ..." : "Listening...";
    };

    recognition.onend = () => {
        isListening = false;
        micButton.classList.remove('listening');
        if (statusDiv.textContent.includes("Listening") || statusDiv.textContent.includes("सुन रहा")) {
            statusDiv.textContent = currentLang === 'hi-IN' ? "बोलने के लिए क्लिक करें" : "Click mic or type to chat";
        }
    };

    recognition.onresult = async (event) => {
        const text = event.results[0][0].transcript;
        handleUserMessage(text);
    };

    recognition.onerror = (event) => {
        console.error("Speech Error:", event.error);
        statusDiv.textContent = "Error: " + event.error;
        isListening = false;
        micButton.classList.remove('listening');
    };
} else {
    statusDiv.textContent = "Voice input not supported in this browser.";
    micButton.disabled = true;
}

// Event Listeners
micButton.addEventListener('click', () => {
    if (!recognition) return;
    if (isListening) {
        recognition.stop();
    } else {
        recognition.start();
    }
});

sendButton.addEventListener('click', () => {
    const text = textInput.value.trim();
    if (text) {
        handleUserMessage(text);
        textInput.value = '';
    }
});

textInput.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
        const text = textInput.value.trim();
        if (text) {
            handleUserMessage(text);
            textInput.value = '';
        }
    }
});

stopButton.addEventListener('click', () => {
    window.speechSynthesis.cancel();
    statusDiv.textContent = currentLang === 'hi-IN' ? "रुका हुआ" : "Stopped";
    visualizer.classList.add('hidden');
});

langToggle.addEventListener('change', (e) => {
    if (e.target.checked) {
        currentLang = 'hi-IN';
        statusDiv.textContent = "हिंदी मोड सक्रिय";
        textInput.placeholder = "संदेश टाइप करें...";
    } else {
        currentLang = 'en-US';
        statusDiv.textContent = "English Mode Active";
        textInput.placeholder = "Type a message...";
    }
    if (recognition) recognition.lang = currentLang;
});

// Core Logic
async function handleUserMessage(text) {
    addMessage(text, 'user');
    statusDiv.textContent = currentLang === 'hi-IN' ? "सोच रहा हूँ..." : "Thinking...";

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message: text, language: currentLang })
        });

        const data = await response.json();

        if (data.error) throw new Error(data.error);

        addMessage(data.reply, 'ai');
        speak(data.reply);
        statusDiv.textContent = currentLang === 'hi-IN' ? "तैयार" : "Ready";

    } catch (error) {
        console.error("API Error:", error);
        statusDiv.textContent = "Error getting response";
        addMessage("Sorry, I encountered an error.", 'ai');
    }
}

function addMessage(text, sender) {
    const div = document.createElement('div');
    div.className = `message ${sender}-message`;
    div.textContent = text;
    chatHistory.appendChild(div);
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function speak(text) {
    if (!window.speechSynthesis) return;

    statusDiv.textContent = currentLang === 'hi-IN' ? "बोल रहा हूँ..." : "Speaking...";
    visualizer.classList.remove('hidden');

    // Cancel any current speech
    window.speechSynthesis.cancel();

    const utterance = new SpeechSynthesisUtterance(text);

    const voices = window.speechSynthesis.getVoices();
    let preferredVoice = null;

    if (currentLang === 'hi-IN') {
        // Try to find a Hindi voice
        preferredVoice = voices.find(v => v.lang.includes('hi') || v.name.includes('Hindi'));
    } else {
        // English voice
        preferredVoice = voices.find(v => v.name.includes("Google US English") || v.name.includes("Samantha"));
    }

    if (preferredVoice) utterance.voice = preferredVoice;
    utterance.lang = currentLang;

    utterance.onend = () => {
        statusDiv.textContent = currentLang === 'hi-IN' ? "तैयार" : "Click mic or type to chat";
        visualizer.classList.add('hidden');
    };

    window.speechSynthesis.speak(utterance);
}
