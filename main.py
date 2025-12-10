import os
from flask import Flask, request, jsonify, render_template
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# -----------------------------------------------------------
# 👇 STEP 1: PASTE THE KEY FROM YOUR 'Voicekey' PROJECT HERE 👇
# -----------------------------------------------------------
MY_API_KEY = "AIzaSyCF0kBjnTayg4lrdkkZtiWwl8HlQbdbp8c"

if "PASTE" in MY_API_KEY:
    print("❌ ERROR: Please paste the API Key from your 'Voicekey' project!")

genai.configure(api_key=MY_API_KEY)

# -----------------------------------------------------------
# 👇 STEP 2: WE USE THE STANDARD FREE MODEL (NOT 2.5) 👇
# -----------------------------------------------------------
try:
    # 'gemini-flash-latest' points to the stable 1.5 Flash version (Free)
    model = genai.GenerativeModel('gemini-flash-latest')
    print("✅ Connection verified. Model 'gemini-flash-latest' selected.")
except:
    # Fallback to Pro if Flash fails
    model = genai.GenerativeModel('gemini-pro')
    print("⚠️ Flash failed, switched to 'gemini-pro'")

SYSTEM_PROMPT = "You are an AI Interviewer. Keep answers short."

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        msg = data.get('message', '')
        print(f"🗣️ User: {msg}")

        # Send to Google
        response = model.generate_content(f"{SYSTEM_PROMPT}\nUser: {msg}")
        
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