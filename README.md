# AI Interviewer Voice Bot

This project is an AI-powered Voice Bot designed to represent a candidate for an AI Engineer role. It uses Google's Gemini Flash model to generate concise, spoken-style responses suitable for voice interaction.

## Features

-   **Persona-based AI**: Represents a specific candidate profile with a defined background, superpowers, and goals.
-   **Voice-Optimized Responses**: Generates short, 2-3 sentence answers ideal for text-to-speech.
-   **Multi-language Support**: Detects Hindi input and responds in Hinglish (Hindi + English) for natural conversation.
-   **Real-time Interaction**: Built with Flask for low-latency responses.

## Tech Stack

-   **Backend**: Python, Flask
-   **AI Model**: Google Gemini 1.5 Flash (`gemini-2.5-flash`)
-   **Frontend**: HTML/JS (served via Flask static files)

## Setup & Installation

1.  **Clone the repository**
    ```bash
    git clone https://github.com/sanskarr16/VoiceBot.git
    cd VoiceBot
    ```

2.  **Create a virtual environment**
    ```bash
    python -m venv .venv
    # Windows
    .venv\Scripts\activate
    # Mac/Linux
    source .venv/bin/activate
    ```

3.  **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up Environment Variables**
    Create a `.env` file in the root directory and add your Gemini API key:
    ```env
    GEMINI_API_KEY=your_api_key_here
    ```

## Usage

1.  **Run the application**
    ```bash
    python main.py
    ```
2.  Open your browser and navigate to `http://localhost:5000`.
3.  Start chatting!

## Project Structure

-   `main.py`: Main Flask application and AI logic.
-   `static/`: Contains frontend assets (HTML, CSS, JS).
-   `requirements.txt`: Python dependencies.
