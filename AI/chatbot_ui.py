from openai import OpenAI
import gradio as gr

OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

MODEL = "llama3.2"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


# Chatbot can be initiated using single line of code:
# gr.load_chat(OLLAMA_BASE_URL, model=MODEL, token="***").launch()

system_prompt = "You are helpful assistant"


def chat(message, history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history + [{"role": "user", "content": message}]

    stream = ollama.chat.completions.create(messages=messages, model=MODEL, stream=True)

    response = ""

    for chunk in stream:
        response += chunk.choices[0].delta.content or ''
        yield response


gr.ChatInterface(chat).launch()
