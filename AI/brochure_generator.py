from openai import OpenAI
import gradio as gr
from bs4 import BeautifulSoup
import requests

OLLAMA_BASE_URL = "http://127.0.0.1:11434/v1"
ollama = OpenAI(base_url=OLLAMA_BASE_URL, api_key="ollama")


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def generate_brochure(website_name, website_url, model):

    web_content = fetch_website_contents(website_url)

    user_prompt = f"""
    Provided content of website named {website_name} and content below.
    Make a sales brochure. Return response in mark down.
    <web-content-start>
    {web_content}
    <web-content-end>
    """

    messages = [
        {"role": "system", "content": "You are sales expert"},
        {"role": "user", "content": user_prompt},
    ]

    stream = ollama.chat.completions.create(
        messages=messages,
        model=model,
        stream=True,
    )

    response = ""

    for chunk in stream:
        response += chunk.choices[0].delta.content or ""
        yield response


name_input = gr.Textbox(label="Company name:")
url_input = gr.Textbox(label="Landing page URL including http:// or https://")
model_selector = gr.Dropdown(
    ["llama3.2", "phi3"],
    label="Select model",
    value="llama3.2",
)
message_output = gr.Markdown(label="Response:")

view = gr.Interface(
    fn=generate_brochure,
    title="Brochure Generator",
    inputs=[name_input, url_input, model_selector],
    outputs=[message_output],
    examples=[
        ["Vivek Sudani", "https://www.linkedin.com/in/viveksudani/", "llama3.2"],
        ["Vivek Sudani", "https://github.com/viveksudani", "phi3"],
        ["Hugging Face", "https://huggingface.co", "llama3.2"],
    ],
    flagging_mode="never",
)

view.launch()
