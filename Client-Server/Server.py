from langchain.prompts import ChatPromptTemplate
from langchain.chat_models import ChatOpenAI
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from langserve import add_routes

import uvicorn
import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY")

# Initialize FastAPI app
app = FastAPI(
    title="Langchain Server",
    version="1.0",
    description="A simple API server for interacting with multiple LLMs"
)

# Step 1: Initialize Language Models

# OpenAI GPT-3.5 Turbo
chatgpt3_5 = ChatOpenAI(model="gpt-3.5-turbo")

# Google Generative AI (Gemini 1.5 Pro)
gemini = ChatGoogleGenerativeAI(model="gemini-1.5-pro")

# Ollama Llama 3.2
llama3_2 = Ollama(model="llama3.2")

# Step 2: Define Prompt Template
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful assistant. Please respond to user queries."),
        ("user", "Question: {question}")
    ]
)

# Step 3: Add routes for each LLM
app.mount(
    "/static", 
    StaticFiles(directory="static"), 
    name="static"
)

# Home endpoint to serve index.html
@app.get("/", response_class=FileResponse)
async def read_index():
    return "static/index.html"

add_routes(
    app,
    prompt | chatgpt3_5,
    path="/chat_with_gpt"
)

add_routes(
    app,
    prompt | gemini,
    path="/chat_with_gemini"
)

add_routes(
    app,
    prompt | llama3_2,
    path="/chat_with_llama"
)

# Entry point
if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)
