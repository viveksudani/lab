from openai import OpenAI


OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

MODEL = "llama3.2"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

messages = []

while True:
    user_input = input("Your message:")

    if user_input == "":
        print("exited")
        break

    print("User:", user_input)

    messages.append(
        {
            "role": "user",
            "content": user_input,
        }
    )

    completion = ollama.chat.completions.create(
        model=MODEL,
        messages=messages,
    )

    ai_response = completion.choices[0].message.content

    print("AI:", ai_response)

    messages.append(
        {
            "role": "assistant",
            "content": ai_response,
        }
    )
