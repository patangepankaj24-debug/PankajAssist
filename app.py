from flask import Flask, render_template, request, jsonify
import requests
import os

app = Flask(__name__)

GROQ_API_KEY = "your_groq_api_key_here"
MODEL = "llama3-70b-8192"  # Or mixtral or gemma depending on your choice

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get('message')

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are Pankaj Assist, a helpful and sometimes funny chatbot."},
            {"role": "user", "content": user_message}
        ]
    }

    response = requests.post("https://api.groq.com/openai/v1/chat/completions", headers=headers, json=data)

    if response.status_code == 200:
        reply = response.json()['choices'][0]['message']['content']
        return jsonify({'reply': reply})
    else:
        return jsonify({'reply': "Oops! Something went wrong."}), 500

if __name__ == '__main__':
    app.run(debug=True)
