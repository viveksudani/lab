import os
import json
import sqlite3
import base64

from dotenv import load_dotenv
from openai import OpenAI
import gradio as gr
from io import BytesIO
from PIL import Image


load_dotenv(override=True)

openai_api_key = os.getenv("OPENAI_API_KEY")
MODEL = "gpt-4.1-mini"

openai = OpenAI(api_key=openai_api_key)


system_prompt = """
You are helpful airline assistant. Give short answers, no more than 1 sentence.
Always be accurate. If you don't know the answer, say so.
"""


print("setting tickets database...")

DB = "prices.db"

# Create db if doesn't exist
with sqlite3.connect(DB) as conn:
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS prices (city TEXT PRIMARY KEY, price REAL)"
    )
    conn.commit()


def set_ticket_price(city, price):
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO prices (city, price) VALUES (?, ?) ON CONFLICT(city) DO UPDATE SET price = ?",
            (city.lower(), price, price),
        )
        conn.commit()


print("Loading ticket prices in db....")

ticket_prices = {"london": 799, "paris": 899, "tokyo": 1420, "sydney": 2999}
for city, price in ticket_prices.items():
    set_ticket_price(city, price)


def get_ticket_price(city):
    print(f"DATABASE TOOL CALLED: Getting price for {city}", flush=True)
    with sqlite3.connect(DB) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT price FROM prices WHERE city = ?", (city.lower(),))
        result = cursor.fetchone()
        return (
            f"Ticket price to {city} is ${result[0]}"
            if result
            else "No price data available for this city"
        )


print("Preparing LLM tool for ticket_price...")
price_function = {
    "name": "get_ticket_price",
    "description": "Get the price of a return ticket to the destination city.",
    "parameters": {
        "type": "object",
        "properties": {
            "destination_city": {
                "type": "string",
                "description": "The city that the customer wants to travel to",
            },
        },
        "required": ["destination_city"],
        "additionalProperties": False,
    },
}
tools = [{"type": "function", "function": price_function}]


print("Setting image artist...")


def artist(city):
    image_response = openai.images.generate(
        model="dall-e-3",
        prompt=f"An image representing a vacation in {city}, showing tourist spots and everything unique about {city}, in a vibrant pop-art style",
        size="1024x1024",
        n=1,
        response_format="b64_json",
    )
    image_base64 = image_response.data[0].b64_json
    image_data = base64.b64decode(image_base64)
    return Image.open(BytesIO(image_data))


print("Setting audio agent...")


def talker(message):
    response = openai.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="onyx",
        input=message,
    )
    return response.content


def handle_tool_calls_and_return_cities(message):
    responses = []
    cities = []
    for tool_call in message.tool_calls:
        if tool_call.function.name == "get_ticket_price":
            arguments = json.loads(tool_call.function.arguments)
            city = arguments.get("destination_city")
            cities.append(city)
            price_details = get_ticket_price(city)
            responses.append(
                {"role": "tool", "content": price_details, "tool_call_id": tool_call.id}
            )
    return responses, cities


def chat(history):
    history = [{"role": h["role"], "content": h["content"]} for h in history]
    messages = [{"role": "system", "content": system_prompt}] + history

    response = openai.chat.completions.create(
        model=MODEL, messages=messages, tools=tools
    )
    cities = []
    image = None

    while response.choices[0].finish_reason == "tool_calls":
        message = response.choices[0].message
        responses, cities = handle_tool_calls_and_return_cities(message)
        messages.append(message)
        messages.extend(responses)
        response = openai.chat.completions.create(
            model=MODEL, messages=messages, tools=tools
        )

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
