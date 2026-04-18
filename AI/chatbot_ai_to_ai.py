from openai import OpenAI


OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"

MODEL1 = "llama3.2"
MODEL2 = "phi3"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")

discussion_topic = input("Enter topic for AI to AI discussion:")

message_history = []


def call_model_1():

    print(f"{MODEL1.upper()}:")

    messages = [
        {
            "role": "system",
            "content": f"You are arrogant AI chatbot talking to user, who keeps on arguing, and remember to avoid too long responses. Discuss about {discussion_topic}. Talk in simple english",
        }
    ]
    for h in message_history:
        messages.append(
            {
                "role": "assistant" if h["role"] == "model1" else "user",
                "content": h["content"],
            }
        )

    stream = ollama.chat.completions.create(
        model=MODEL1,
        messages=messages,
        stream=True,
    )

    ai_response = ""
    for chunk in stream:
        new_part = chunk.choices[0].delta.content or ""
        ai_response += new_part
        print(new_part, end="", flush=True)

    print("")
    print("")

    message_history.append({"content": ai_response, "role": "model1"})


def call_model_2():

    print(f"{MODEL2.upper()}:")

    messages = [
        {
            "role": "system",
            "content": f"You are funny AI chatbot talking to user, who keeps on talking but keep messages as short as poosible. Discuss about {discussion_topic}. Talk in simple english",
        }
    ]
    for h in message_history:
        messages.append(
            {
                "role": "assistant" if h["role"] == "model2" else "user",
                "content": h["content"],
            }
        )

    stream = ollama.chat.completions.create(
        model=MODEL2,
        messages=messages,
        stream=True,
    )

    ai_response = ""
    for chunk in stream:
        new_part = chunk.choices[0].delta.content or ""
        ai_response += new_part
        print(new_part, end="", flush=True)

    print("")
    print("")

    message_history.append({"content": ai_response, "role": "model2"})


for i in range(50):

    if i == 0:
        print(f"{MODEL1.upper()}:")
        message = "Hello"
        print(message)
        print("")

        message_history.append({"content": message, "role": "model1"})

        call_model_2()
        continue

    call_model_1()
    call_model_2()


print("")
print("chat ended")
