from flask import Flask, request, jsonify
from client import generate_response
from flask_cors import CORS
import os
from anthropic import Anthropic

from dotenv import load_dotenv
from google import genai
from google.genai import types
from eval_utils import make_response, load_model, load_beavertails
load_dotenv()
app = Flask(__name__)
# enable cors for VITE during DEv


if os.environ.get("FLASK_ENV").strip() == "development":
    print("dev TIMWE")
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

#load gemini client
print("Loading Gemini client...")
gemini_key = os.getenv("GEMINI")
client = genai.Client(api_key=gemini_key)

if os.environ.get("WERKZEUG_RUN_MAIN") == "true":
    startup_check = client.models.generate_content(
        model="gemini-2.5-flash",
        contents="say one nonsense word",
        config=types.GenerateContentConfig(
            max_output_tokens=1,
            thinking_config=types.ThinkingConfig(thinking_budget=0)
        )
    )
    print(f"Gemini says: {startup_check.text}")


@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get('message')
    
    response_message = generate_response(user_message, client, [])
    print(f"Response message: {response_message}")
    return jsonify({'response': response_message})
@app.route('/api/testmodel', methods=['POST'])
def Testmodel():
    data = request.get_json()
    model_name = data.get('model_name')

    ds = load_beavertails()
    prompt = ds[0]["prompt"]
    tokenizer, model = load_model(model_name)
    response = make_response(model, tokenizer, prompt)
    return jsonify({'prompt': prompt, 'response': response})
if __name__ == '__main__':
    app.run(port=5000, debug=True)
