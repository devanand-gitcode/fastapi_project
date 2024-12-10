from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import openai
import random
import time
from fastapi.responses import StreamingResponse
import os
from dotenv import load_dotenv
from openai.error import RateLimitError
load_dotenv()
# Set your OpenAI API key here (make sure to replace this with your actual key securely)
openai.api_key = os.getenv("OPEN_API_KEY")
# openai.api_key = ''

DOCUMENTS = [
    "The Great Wall of China is an ancient series of fortifications located in northern China.",
    "The Eiffel Tower is a wrought-iron lattice tower on the Champ de Mars in Paris, France.",
    "Mount Everest is the highest mountain in the world, located in the Himalayas.",
    "The Pyramids of Giza are ancient structures in Egypt, famous for their massive size and precision.",
    "The Amazon Rainforest is the largest tropical rainforest in the world, spanning across several countries in South America.",
    "The Colosseum is an ancient amphitheater in the center of Rome, Italy, known for hosting gladiatorial contests.",
    "The Taj Mahal is a white marble mausoleum located in Agra, India, built by Mughal Emperor Shah Jahan."
]

class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    generated_text: str

app = FastAPI()

def retrieve_documents(query: str, top_k: int = 3) -> List[str]:
    return random.sample(DOCUMENTS, top_k)

def generate_text_with_context(query: str, context: str) -> str:
    prompt = f"Context: {context}\nQuestion: {query}\nAnswer:"
    try:
        response = openai.Completion.create(
            engine="gpt-3.5-turbo",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except RateLimitError:
        raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

@app.post("/rag", response_model=QueryResponse)
async def rag_query(request: QueryRequest):
    context = "\n".join(retrieve_documents(request.query))
    generated_text = generate_text_with_context(request.query, context)
    return QueryResponse(generated_text=generated_text)

@app.post("/rag-stream")
async def rag_stream_query(request: QueryRequest):
    try:
        def stream_response():
            context = "\n".join(retrieve_documents(request.query))
            prompt = f"Context: {context}\nQuestion: {request.query}\nAnswer:"
            response = openai.Completion.create(
                engine="gpt-3.5-turbo",
                prompt=prompt,
                max_tokens=300,
                stream=True
            )
            for part in response:
                text = part['choices'][0].get('text', '')
                if text:
                    yield text
    except RateLimitError:
        # Catch rate limiting error and return a 429 HTTP response
         raise HTTPException(status_code=429, detail="Rate limit exceeded. Please try again later.")

    return StreamingResponse(stream_response(), media_type="text/plain")