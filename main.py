import os
from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
import pathlib
import textwrap

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import whisper


app = FastAPI()
# ------------start---------------
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)

# LOAD WHISPER MODEL
model = whisper.load_model("base")

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
for m in genai.list_models():
  if 'generateContent' in m.supported_generation_methods:
    print(m.name)


# ----------------end----------------
@app.get("/")
async def root():
    return {"message": "Hello World"}

@app.post("/talk")
async def post_audio():
    audio_file = open("recording.mp3")
    transcript = model.transcribe(audio_file)

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    return {"filename": file.filename}