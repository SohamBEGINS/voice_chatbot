import os
os.environ["PATH"] += os.pathsep + "C:\\ffmpeg"  # Adjust the path as necessary



import elevenlabs
from elevenlabs import play
from elevenlabs.client import ElevenLabs

client = ElevenLabs(
  api_key="sk_11a437000b50f2c25fc7e1baff7ccf40529f3de7b7356844", # Defaults to ELEVEN_API_KEY or ELEVENLABS_API_KEY
)

audio = client.generate(
  text="Hello! 你好! Hola! नमस्ते! Bonjour! こんにちは! مرحبا! 안녕하세요! Ciao! Cześć! Привіт! வணக்கம்!",
  voice="Brian",
  model="eleven_multilingual_v2"
)
play(audio)