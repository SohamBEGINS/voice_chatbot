# Flask Application Code

from flask import Flask, request, jsonify, render_template
import os
import time
import google.generativeai as genai
from elevenlabs import ElevenLabs

app = Flask(__name__)

# Leave space for API keys
GOOGLE_API_KEY = "AIzaSyDOFyCQCevseNgTzgKCwQgbKr6ufMnj4nY"
ELEVEN_API_KEY = "sk_11a437000b50f2c25fc7e1baff7ccf40529f3de7b7356844"

genai.configure(api_key=GOOGLE_API_KEY)
elevenlabs_client = ElevenLabs(api_key=ELEVEN_API_KEY)

os.makedirs("static/recordings", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message", "").strip()

    # Validate input
    if not user_input:
        return jsonify({"reply": "I'm sorry, I didn't catch that. Please try again.", "audio_url": None})

    selected_model = data.get("model", "gemini-2.0-flash-exp")

    try:
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(user_input)
        chatbot_reply = response.text or "I'm sorry, I couldn't process that."
    except Exception as e:
        chatbot_reply = f"Error: {e}"

    try:
        audio_stream = elevenlabs_client.generate(
            text=chatbot_reply,
            voice="Xb7hH8MSUJpSbSDYk0k2",
            model="eleven_multilingual_v2"
        )
        audio_bytes = b"".join(audio_stream)
        unique_filename = f"static/recordings/response_{int(time.time())}.mp3"

        with open(unique_filename, "wb") as f:
            f.write(audio_bytes)

    except Exception as e:
        chatbot_reply += f"\n[Note: Eleven Labs Error: {e}]"
        unique_filename = None

    return jsonify({"reply": chatbot_reply, "audio_url": unique_filename})


@app.route("/greet", methods=["POST"])
def greet():
    data = request.json
    user_name = data.get("name")

    # Generate personalized greeting
    chatbot_reply = f"<break time='500ms'/>Hi.<break time='500ms'/> {user_name}</speak>"


    # Generate audio using ElevenLabs
    try:
        audio_stream = elevenlabs_client.generate(
            text=chatbot_reply,
            voice="Xb7hH8MSUJpSbSDYk0k2",
            model="eleven_multilingual_v2"
        )
        audio_bytes = b"".join(audio_stream)
        unique_filename = f"static/recordings/greeting_{int(time.time())}.mp3"

        with open(unique_filename, "wb") as f:
            f.write(audio_bytes)
    except Exception as e:
        chatbot_reply += f" [Note: Eleven Labs Error: {e}]"
        unique_filename = None

    return jsonify({"reply": chatbot_reply, "audio_url": unique_filename})


if __name__ == "__main__":
    app.run(debug=True)
