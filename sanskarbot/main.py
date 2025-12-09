import os
from flask import Flask, request, jsonify, send_from_directory
import google.generativeai as genai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static')

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("⚠️ WARNING: GEMINI_API_KEY not found in .env file!")

genai.configure(api_key=api_key)
model = genai.GenerativeModel('gemini-2.5-flash')

SYSTEM_PROMPT = """
You are an AI Voice Bot representing a candidate for an AI Engineer role at 100x.
Answer questions as if you are the candidate. Keep answers concise (2-3 sentences max) because they will be spoken aloud.

Here is your persona and context:
1. **Life Story**: I started coding games in high school, fell in love with AI during my CS degree, and have been building agentic workflows for the last 3 years. I love turning complex research into shipping products.
2. **Superpower**: My speed of iteration. I can prototype a new idea in hours, not days, which helps us find the right solution faster.
3. **Areas to Grow**: Engineering leadership, public speaking, and deepening my knowledge of lower-level model optimization.
4. **Misconception**: That I only care about code. I'm actually deeply product-focused and care about the user experience first.
5. **Pushing Boundaries**: I sign up for hackathons with tools I've never used before, forcing myself to learn under pressure.

Tone: Professional, enthusiastic, confident, but humble.
"""

@app.route('/')
def index():
    return send_from_directory('static', 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    user_message = data.get('message', '')
    language = data.get('language', 'en-US')

    # --- TERMINAL LOGGING (USER) ---
    print(f"\n🗣️  [USER] ({language}): {user_message}")

    try:
        current_prompt = SYSTEM_PROMPT
        if language == 'hi-IN':
            current_prompt += "\n\nIMPORTANT: The user is speaking in Hindi. Please reply in Hindi (Devanagari script) mixed with some English terms (Hinglish) to sound natural. Keep it professional yet conversational."

        chat_session = model.start_chat(history=[])
        response = chat_session.send_message(f"{current_prompt}\n\nUser Question: {user_message}")
        reply_text = response.text

        # --- TERMINAL LOGGING (AI) ---
        print(f"🤖 [AI]: {reply_text}\n")

        return jsonify({"reply": reply_text})

    except Exception as e:
        error_msg = str(e)
        print(f"❌ [ERROR]: {error_msg}")
        return jsonify({"error": "Failed to generate response"}), 500

if __name__ == '__main__':
    print("🚀 Server starting on http://localhost:5000")
    app.run(host='0.0.0.0', port=5000, debug=True)
