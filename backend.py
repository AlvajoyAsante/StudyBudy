from fastapi import FastAPI
from pydantic import BaseModel
import os
from groq import Groq  # Correct import

# Initialize FastAPI
app = FastAPI()

# Set up Groq client
groq_client = Groq(api_key="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")

class Transcript(BaseModel):
    content: str

class Question(BaseModel):
    question: str
    transcript: str

# Function to communicate with Groq API
def chat_with_groq(prompt: str) -> str:
    response = groq_client.chat.completions.create(  # <- Correct syntax
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content  # <- Correct response parsing

# Endpoint to summarize lecture
@app.post("/summarize")
def summarize_lecture(transcript: Transcript):
    prompt = f"Summarize the following lecture into key points:\n\n{transcript.content}\n\nSummary:"
    return {"summary": chat_with_groq(prompt)}

# Endpoint to extract key concepts from lecture
@app.post("/key_concepts")
def extract_key_concepts(transcript: Transcript):
    prompt = f"Extract key concepts and definitions from the following lecture:\n\n{transcript.content}\n\nKey Concepts:"
    return {"key_concepts": chat_with_groq(prompt)}

# Endpoint to generate quiz questions
@app.post("/generate_quiz")
def generate_quiz(transcript: Transcript):
    prompt = f"Generate 5 multiple-choice questions based on this lecture:\n\n{transcript.content}\n\nQuiz Questions:"
    return {"quiz_questions": chat_with_groq(prompt)}

# Endpoint to answer student questions
@app.post("/ask")
def ask_question(q: Question):
    prompt = f"Lecture:\n{q.transcript}\n\nQuestion: {q.question}\n\nAnswer:"
    return {"answer": chat_with_groq(prompt)}
