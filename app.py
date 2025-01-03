from flask import Flask, request, jsonify, render_template
import os
import time  # For generating unique filenames
import google.generativeai as genai
from elevenlabs import ElevenLabs

app = Flask(__name__)

# Configure the Google Generative AI SDK
GOOGLE_API_KEY = "AIzaSyDOFyCQCevseNgTzgKCwQgbKr6ufMnj4nY"
genai.configure(api_key=GOOGLE_API_KEY)

# Configure Eleven Labs API
ELEVEN_API_KEY = "sk_11a437000b50f2c25fc7e1baff7ccf40529f3de7b7356844"
elevenlabs_client = ElevenLabs(api_key=ELEVEN_API_KEY)

# Ensure the static folder exists
os.makedirs("static", exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_input = data.get("message")
    selected_model = data.get("model", "gemini-2.0-flash-exp")  # Default model

    try:
        # Load the selected model
        model = genai.GenerativeModel(selected_model)
        response = model.generate_content(user_input)
        chatbot_reply = response.text  # Assuming the response contains the 'text' field
    except Exception as e:
        chatbot_reply = f"Error: {e}"

    try:
        # Generate speech using Eleven Labs
        audio_stream = elevenlabs_client.generate(
            text = f" .. {chatbot_reply}",
            voice="Rachel",  # You can customize the voice
            model="eleven_multilingual_v2",
            optimize_streaming_latency= 2 ,
            
        )

        # Concatenate the bytes from the generator
        audio_bytes = b"".join(audio_stream)

        # Create a unique filename using a timestamp to avoid caching issues
        unique_filename = f"static/response_{int(time.time())}.mp3"

        # Save the audio to the static folder
        with open(unique_filename, "wb") as f:
            f.write(audio_bytes)

    except Exception as e:
        chatbot_reply += f"\n[Note: Eleven Labs Error: {e}]"
        unique_filename = None

    return jsonify({"reply": chatbot_reply, "audio_url": unique_filename})

if __name__ == "__main__":
    app.run(debug=True)
