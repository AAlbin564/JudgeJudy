import gradio as gr
import os
from dotenv import load_dotenv
from google import genai

from client import generate_response

def respond (message, history):
    gemini_key = os.getenv("Gemini")
    print(f"Gemini Key: {gemini_key}")
    client = genai.Client(api_key=gemini_key)
    return generate_response(message, client, history)

load_dotenv()
history = []


demo = gr.ChatInterface(
        fn=respond,
        title="Judge Judy LLM",
        description="Ask Judge Judy anything!",
    )

def main():
    demo.launch()

if __name__ == "__main__":
    main()