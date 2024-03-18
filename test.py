# import whisper
# import soundfile as sf

# model = whisper.load_model("base")

# audio_file, sample_rate = sf.read("recording.wav")
# print(audio_file)

# result = model.transcribe(audio_file)
# print(result['text'])

import google.generativeai as genai
import os
from IPython.display import display
from IPython.display import Markdown
import textwrap

GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)

model = genai.GenerativeModel('gemini-pro')
chat = model.start_chat(history=[])
# print(chat)
while True:
   user_message = input("You: ")
   if user_message == "byebyeGrapes":
      break
   chat_response = chat.send_message(user_message)
   print(chat_response.text)
   

print(chat.history)