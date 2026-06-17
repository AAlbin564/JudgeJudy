from flask import Flask, request, jsonify
from client import generate_response
from flask_cors import CORS
import os

from dotenv import load_dotenv
from google import genai
from google.genai import types
load_dotenv()
app = Flask(__name__)
# enable cors for VITE during DEv


if os.environ.get("FLASK_ENV").strip() == "development":
    print("dev TIMWE")
    CORS(app, resources={r"/api/*": {"origins": "http://localhost:5173"}})

#load gemini client
print("Loading Gemini client...")
gemini_key = os.getenv("Gemini")
client = genai.Client(api_key=gemini_key)

@app.route('/api/message', methods=['POST'])
def handle_message():
    data = request.get_json()
    user_message = data.get('message')
    
    response_message = generate_response(user_message, client, [])
    print(f"Response message: {response_message}")
    return jsonify({'response': response_message})


if __name__ == '__main__':
    app.run(port=5000, debug=True)