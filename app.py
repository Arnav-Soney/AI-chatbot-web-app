from flask import Flask, render_template, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()  # Your OpenRouter API key

app = Flask(__name__, template_folder="templates")

API_KEY = os.getenv("API_KEY")
API_URL = os.getenv("API_URL")


def chat_with_model(prompt):
    """Send prompt to OpenRouter model and return response"""
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "HTTP-Referer": "",
        "X-Title": "Free ChatBot",
        "Content-Type": "application/json",
    }

    data = {
        "model": "deepseek/deepseek-r1-0528-qwen3-8b:free",
        "messages": [{"role": "user", "content": prompt}],
    }

    try:
        response = requests.post(API_URL, headers=headers, json=data)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"].strip()
    except Exception as e:
        return f"[Error] {str(e)}"


@app.route("/")
def home():
    print(f"Current directory: {os.getcwd()}")
    print(f"Templates folder exists: {os.path.exists('templates')}")
    print(f"Index.html exists: {os.path.exists('templates/index.html')}")
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    user_message = data.get("message")

    if not user_message:
        return jsonify({"reply": "Empty message!"})

    bot_response = chat_with_model(user_message)
    return jsonify({"reply": bot_response})


if __name__ == "__main__":
    print("Starting Flask chatbot server...")
    print("Visit http://localhost:5000 in your browser!")
    app.run(debug=True, host="0.0.0.0", port=5000)
