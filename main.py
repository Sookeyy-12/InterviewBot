import json
import os
from fastapi import FastAPI, UploadFile
from dotenv import load_dotenv
import pathlib
import textwrap
import soundfile as sf
import numpy as np

import google.generativeai as genai

from IPython.display import display
from IPython.display import Markdown

import whisper

app = FastAPI()
load_dotenv()

GEMINI_KEY = os.getenv("GEMINI_KEY")
genai.configure(api_key=GEMINI_KEY)

model = whisper.load_model("base")

chatbot = genai.GenerativeModel('gemini-pro')
chat = chatbot.start_chat(history=[])

def to_markdown(text):
    text = text.replace('•', '  *')
    return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
      print(m.name)


@app.get("/")
async def root():
    get_context()
    return {"message": "Hello World"}

@app.post("/talk")
async def post_audio(file: UploadFile):
    user_message = transcribe_audio(file.filename)
    chat_respose = get_chat_response(user_message)
    print(chat_respose)

def transcribe_audio(file):
    transcript = model.transcribe(file)
    return transcript['text']
    # return {"message" : "Audio has been Transcribed."}

def get_chat_response(user_message):
    # messages = load_messages()
    # messages.append(user_message)
    response = chat.send_message(str(user_message))
    # print(response.text)
    return response.text

def get_context():
# Define interview context
    ctx = input("Enter the position you are interviewing for: ")
    resp = chat.send_message(f"Act as an Interviewer for the position {ctx}. You role is to help me prepare for the interview. You have to ask questions that are relevant to the position and evaluate me based on my responses. You can also provide feedback to me. At the end of the interview, provide constructive critisim on my performance. You're name is Grapes. NOTE: You have to ask only one question at a time.")
    print(resp.text)
    return {"message" : "Context has been set."}

# def load_messages():
#     messages = []
#     file = "database.json"
#     empty = os.stat("file").st_size == 0
#     if not empty:
#         with open(file) as db_file:
#             data = json.load(db_file)
#             for item in data:
#                 messages.append(item)
#     else :
#         messages.append(
#             {"role": "system", "content": "You are an Interviewer who is going to interview a candidate for a job. You have to ask questions that are relevant to the candidate and evaluate the candidate based on their responses. You can also provide feedback to the candidate. You're name is Grapes."}
#         )
#     return messages