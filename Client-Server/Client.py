import requests
import streamlit as st

def get_openai_response(input_text):
    response=requests.post("http://localhost:8000/chat_with_gemini/invoke", json={'input':{'question':input_text}})

    return response.json()['output']['content']

def get_gemini_response(input_text):
    response=requests.post( "http://localhost:8000/chat_with_gemini/invoke", json={'input':{'question':input_text}})

    return response.json()['output']

def get_ollama_response(input_text):
    response=requests.post( "http://localhost:8000/chat_with_llama/invoke", json={'input':{'question':input_text}})

    return response.json()['output']


st.title('Langchain Demo')
input_text=st.text_input("Prompt for GPT, Gemini, and LLama")
if input_text:
    output_text = "## OpenAI GPT model" + get_openai_response(input_text)

    output_text = output_text + "\n\n ## Google Gemini model" + get_gemini_response(input_text)

    output_text = output_text + "\n\n ## LLama model" + get_ollama_response(input_text)

    st.write(output_text)