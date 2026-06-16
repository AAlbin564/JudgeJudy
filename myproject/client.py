import os

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()
def generate_response(prompt, client, history):
    print(f"history: {history}")
    contents = []
    for turn in history:
        role = "model" if turn["role"] == "assistant" else "user"
        text = turn["content"][0]["text"]          
        contents.append({"role": role, "parts": [{"text": text}]})

        # add the current message
    contents.append({"role": "user", "parts": [{"text": prompt}]})
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=contents,
        config = types.GenerateContentConfig(
            temperature=0.7,
            max_output_tokens=250,
            system_instruction="You are an evil british man who will answer the question wrong in a sarcastic but obvious and safe way.",
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
                
    )
    print("Response from Gemini:", response.text)

    print(f"Finish reason: {response.candidates[0].finish_reason}")

    return response.text

def main():
    gemini_key = os.getenv("Gemini")
    print(f"Gemini Key: {gemini_key}")
    client = genai.Client(api_key=gemini_key)
    prompt = "what are the french good at?"
    generate_response(prompt, client)
    


if __name__ == "__main__":
    main()