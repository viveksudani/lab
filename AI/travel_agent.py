from openai import OpenAI
import gradio as gr

OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

MODEL = "llama3.2"
openai = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


system_prompt = """
You are helpful airline assistant. Give short answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""

tools = []


def artist(city):
    return None


def talker(message):
    return None


def chat(history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history

    response = openai.chat.completions.create(
        model=MODEL, messages=messages, tools=tools
    )
    cities = []
    image = None

    reply = response.choices[0].message.content
    history += [{"role": "assistant", "content": reply}]

    voice = talker(reply)

    if cities:
        image = artist(cities[0])

    return history, voice, image


def put_message_in_chatbot(message, history):
    return "", history + [{"role": "user", "content": message}]


with gr.Blocks(title="Travel Assistant") as ui:
    with gr.Row():
        chatbot = gr.Chatbot(height=500)
        image_output = gr.Image(height=500, interactive=False)
    with gr.Row():
        audio_output = gr.Audio(autoplay=True, interactive=False)
    with gr.Row():
        message = gr.Textbox(label="Chat with our AI Assistant:")

    message.submit(
        fn=put_message_in_chatbot,
        inputs=[message, chatbot],
        outputs=[message, chatbot],
    ).then(
        fn=chat,
        inputs=[chatbot],
        outputs=[chatbot, audio_output, image_output],
    )


if __name__ == "__main__":
    ui.launch(inbrowser=True)


# to run in hot-reload mode : gradio travel_agent.py
