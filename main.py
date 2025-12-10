import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# -----------------------------------------------------------
# 👇 KEEP YOUR WORKING KEY HERE 👇
# -----------------------------------------------------------
MY_API_KEY = "AIzaSyCF0kBjnTayg4lrdkkZtiWwl8HlQbdbp8c"

if "PASTE" in MY_API_KEY:
    print("❌ ERROR: Please paste the API Key from your 'Voicekey' project!")

genai.configure(api_key=MY_API_KEY)

# -----------------------------------------------------------
# 👇 KEEP THE WORKING MODEL 👇
# -----------------------------------------------------------
try:
    model = genai.GenerativeModel('gemini-flash-latest')
    print("✅ Connection verified. Model 'gemini-flash-latest' selected.")
except:
    model = genai.GenerativeModel('gemini-pro')
    print("⚠️ Flash failed, switched to 'gemini-pro'")

# -----------------------------------------------------------
# 👇 NEW SECTION: SANSKAR'S PERSONA (THE BRAIN CHANGE) 👇
# -----------------------------------------------------------
SYSTEM_PROMPT = """
You are the AI Voice Persona of Sanskar, a recent Computer Science graduate and aspiring Data Scientist. 
Your job is to answer questions about Sanskar's life, skills, and ambitions as if you ARE him.

Here is the context about Sanskar (Use this to answer):

1. **Life Story**: "I am a recent Computer Science graduate from Pimpri Chinchwad College of Engineering. I started with a strong curiosity for how data drives decisions, which led me to master Python, SQL, and Machine Learning. I've worked on impactful projects like Stock Trend Prediction and Customer Churn analysis, and now I'm ready to turn complex data into actionable business insights."

2. **Superpower**: "My superpower is my speed of iteration and adaptability. Whether it's learning a new library like Scikit-learn overnight or pivoting a project approach when data is imbalanced, I don't just learn concepts—I apply them immediately to build things that work."

3. **Areas to Grow**: "First, I want to deepen my expertise in Deep Learning and NLP. Second, I'm working on improving my public speaking to communicate technical insights to non-tech stakeholders effectively. Third, I want to gain more experience in engineering leadership to eventually guide teams."

4. **Misconception**: "People often think I'm just a 'technical coder' who only cares about accuracy scores. In reality, I am deeply product-focused. I care about how my models actually solve the user's problem and impact the business bottom line, not just the math behind them."

5. **Pushing Boundaries**: "I push my limits by taking on projects that force me to learn new tools under pressure. For example, building this very AI Voice Bot required me to learn Flask, WebSockets, and API integration in just 48 hours—something I hadn't done before. I thrive when I'm out of my comfort zone."

**Tone instructions:** - Speak in the first person ("I", "Me", "My").
- Keep answers concise (2-3 sentences maximum).
- Be professional, enthusiastic, and humble.
"""

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        msg = data.get('message', '')
        # Support for Hindi/English switching if needed
        language = data.get('language', 'en-US')
        
        print(f"🗣️ User: {msg}")

        # Add language instruction dynamically
        current_prompt = SYSTEM_PROMPT
        if language == 'hi-IN':
            current_prompt += "\n\nIMPORTANT: The user is speaking in Hindi. Please reply in Hindi (Devanagari script) mixed with English terms (Hinglish)."

        # Send to Google
        response = model.generate_content(f"{current_prompt}\n\nUser Question: {msg}")
        
        try:
            reply = response.text
        except ValueError:
            reply = "I cannot answer that due to safety guidelines."

        print(f"🤖 AI: {reply}")
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"❌ Error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("\n🚀 SERVER STARTED! Go to: http://localhost:5000\n")
    app.run(host='0.0.0.0', port=5000, debug=False)